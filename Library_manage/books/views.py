from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import Book, Category, BorrowingRecord, Order
from reviews.models import Review
from .forms import BookSearchForm, BorrowBookForm, OrderForm, BookForm
from reviews.forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count
from .services import GoogleBooksService

def book_list(request):
    books = Book.objects.all().order_by('title')
    categories = Category.objects.all()
    search_form = BookSearchForm(request.GET)
    google_books_results = []
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        
        # Search local database
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__icontains=query)
            )
        
        if category:
            books = books.filter(category=category)
            
            # Search Google Books API
            try:
                google_books_service = GoogleBooksService()
                # Get category name and convert to Google Books subject format
                category_name = category.name.lower().replace(' ', '_')
                # If there's a query, combine it with category, otherwise just search by category
                search_query = f"subject:{category_name}" if not query else f"{query} subject:{category_name}"
                google_books_results = google_books_service.search_books(
                    query=search_query,
                    max_results=20  # Increase results for category searches
                )
            except Exception as e:
                messages.warning(request, f'Could not fetch results from Google Books: {str(e)}')
        elif query:  # Only search Google Books if there's a query but no category
            try:
                google_books_service = GoogleBooksService()
                google_books_results = google_books_service.search_books(query=query)
            except Exception as e:
                messages.warning(request, f'Could not fetch results from Google Books: {str(e)}')
    
    # Pagination for local books
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'categories': categories,
        'search_form': search_form,
        'google_books_results': google_books_results,
    }
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    is_available = book.available_copies > 0
    can_borrow = request.user.is_authenticated and request.user.is_student and is_available
    
    # Check if user has already borrowed this book
    has_borrowed = False
    if request.user.is_authenticated:
        has_borrowed = BorrowingRecord.objects.filter(
            book=book,
            borrower=request.user,
            status='BORROWED'
        ).exists()
    
    if request.method == 'POST' and request.user.is_authenticated and request.user.role == 'STUDENT':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('books:detail', pk=book.pk)
    else:
        review_form = ReviewForm()
    
    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'review_form': review_form,
        'is_available': is_available,
        'can_borrow': can_borrow,
        'has_borrowed': has_borrowed,
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def borrow_book(request, pk):
    if not request.user.is_student:
        messages.error(request, 'Only students can borrow books.')
        return redirect('books:list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if book.available_copies <= 0:
        messages.error(request, 'This book is not available for borrowing.')
        return redirect('books:detail', pk=pk)
    
    # Check if user has already borrowed this book
    if BorrowingRecord.objects.filter(book=book, borrower=request.user, status='BORROWED').exists():
        messages.error(request, 'You have already borrowed this book.')
        return redirect('books:detail', pk=pk)
    
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            borrowing_record = form.save(commit=False)
            borrowing_record.book = book
            borrowing_record.borrower = request.user
            borrowing_record.due_date = timezone.now() + timedelta(days=14)  # 2 weeks borrowing period
            borrowing_record.save()
            
            # Update available copies
            book.available_copies -= 1
            book.save()
            
            messages.success(request, 'Book borrowed successfully!')
            return redirect('books:my_books')
    else:
        form = BorrowBookForm()
    
    context = {
        'book': book,
        'form': form,
    }
    return render(request, 'books/borrow_book.html', context)

@login_required
def my_books(request):
    if not request.user.is_student:
        messages.error(request, 'Only students can view their borrowed books.')
        return redirect('books:list')
    
    borrowed_books = BorrowingRecord.objects.filter(
        borrower=request.user,
        status='BORROWED'
    ).select_related('book')
    
    context = {
        'borrowed_books': borrowed_books,
    }
    return render(request, 'books/my_books.html', context)

@login_required
def return_book(request, pk):
    borrowing_record = get_object_or_404(BorrowingRecord, pk=pk, borrower=request.user)
    
    if borrowing_record.status != 'BORROWED':
        messages.error(request, 'This book has already been returned.')
        return redirect('books:my_books')
    
    # Calculate fine if overdue
    if timezone.now() > borrowing_record.due_date:
        days_overdue = (timezone.now() - borrowing_record.due_date).days
        fine = days_overdue * 1.00  # $1 per day fine
        borrowing_record.fine_amount = fine
        request.user.fine_balance += fine
        request.user.save()
    
    # Update borrowing record
    borrowing_record.status = 'RETURNED'
    borrowing_record.return_date = timezone.now()
    borrowing_record.save()
    
    # Update available copies
    book = borrowing_record.book
    book.available_copies += 1
    book.save()
    
    messages.success(request, 'Book returned successfully!')
    return redirect('books:my_books')

def home(request):
    """Main page for regular users and unauthenticated visitors"""
    # Get featured books (most borrowed books)
    featured_books = Book.objects.annotate(
        borrow_count=Count('borrowing_records')
    ).order_by('-borrow_count')[:6]
    
    # Get recent books
    recent_books = Book.objects.order_by('-created_at')[:6]
    
    # Get popular categories
    popular_categories = Category.objects.annotate(
        book_count=Count('books')
    ).order_by('-book_count')[:5]
    
    context = {
        'featured_books': featured_books,
        'recent_books': recent_books,
        'popular_categories': popular_categories,
    }
    return render(request, 'books/home.html', context)

class OrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'books/order_list.html'
    context_object_name = 'orders'
    
    def test_func(self):
        return self.request.user.is_manager
    
    def get_queryset(self):
        return Order.objects.filter(manager=self.request.user)

class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'books/order_form.html'
    success_url = reverse_lazy('books:order_list')
    
    def test_func(self):
        return self.request.user.is_manager
    
    def form_valid(self, form):
        form.instance.manager = self.request.user
        messages.success(self.request, 'Order created successfully!')
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'books/order_form.html'
    success_url = reverse_lazy('books:order_list')
    
    def test_func(self):
        return self.request.user.is_manager and self.get_object().manager == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Order updated successfully!')
        return super().form_valid(form)

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # Check if user is a manager
    if not request.user.is_manager:
        messages.error(request, 'Only managers can delete books.')
        return redirect('books:detail', pk=pk)
    
    # Check if book is currently borrowed
    if BorrowingRecord.objects.filter(book=book, status='BORROWED').exists():
        messages.error(request, 'Cannot delete book that is currently borrowed.')
        return redirect('books:detail', pk=pk)
    
    # Delete the book
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('books:list')

@login_required
def add_book(request):
    if not request.user.role == 'LIBRARIAN':
        messages.error(request, 'Only librarians can add books.')
        return redirect('books:list')
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.available_copies = book.total_copies
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('books:detail', pk=book.pk)
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'title': 'Add New Book'
    }
    return render(request, 'books/book_form.html', context)

@login_required
def import_google_book(request, google_books_id):
    if not request.user.is_manager:
        messages.error(request, 'Only managers can import books.')
        return redirect('books:list')
    
    try:
        google_books_service = GoogleBooksService()
        book_data = google_books_service.get_book_details(google_books_id)
        
        if not book_data:
            messages.error(request, 'Could not find book details.')
            return redirect('books:list')
        
        # Create a new book in the library
        book = Book.objects.create(
            title=book_data['title'],
            author=', '.join(book_data['authors']),
            isbn=book_data['isbn'],
            description=book_data['description'],
            total_copies=1,
            available_copies=1,
            published_date=book_data['published_date']
        )
        
        messages.success(request, f'Successfully imported "{book.title}" into the library.')
        return redirect('books:detail', pk=book.pk)
    
    except Exception as e:
        messages.error(request, f'Error importing book: {str(e)}')
        return redirect('books:list')
