from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta, datetime
from books.models import Book, Category, BorrowingRecord
from books.services import GoogleBooksService
from account.models import User
from .forms import BookForm, CategoryForm
import logging

logger = logging.getLogger(__name__)

def is_librarian(user):
    return user.is_authenticated and user.role == 'LIBRARIAN'

@login_required
@user_passes_test(is_librarian)
def dashboard(request):
    # Get total books count
    total_books = Book.objects.count()
    
    # Get available books count (not currently borrowed)
    available_books = Book.objects.filter(available_copies__gt=0).count()
    
    # Get active borrowings count
    active_borrowings = BorrowingRecord.objects.filter(
        status='BORROWED'
    ).count()
    
    # Get pending fines (overdue books)
    pending_fines = BorrowingRecord.objects.filter(
        status='BORROWED',
        due_date__lt=timezone.now()
    ).aggregate(total_fines=Sum('fine_amount'))['total_fines'] or 0
    
    # Get recent activity (last 10 borrowing records)
    recent_activity = BorrowingRecord.objects.select_related(
        'book', 'borrower'
    ).order_by('-borrowed_date')[:10]
    
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'active_borrowings': active_borrowings,
        'pending_fines': pending_fines,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'librarians/dashboard.html', context)

@login_required
@user_passes_test(is_librarian)
def manage_books(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'librarians/manage_books.html', context)

@login_required
@user_passes_test(is_librarian)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('librarians:manage_books')
    else:
        form = BookForm()
    
    context = {
        'form': form,
    }
    return render(request, 'librarians/book_form.html', context)

@login_required
@user_passes_test(is_librarian)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('librarians:manage_books')
    else:
        form = BookForm(instance=book)
    
    context = {
        'book': book,
        'form': form,
    }
    return render(request, 'librarians/book_form.html', context)

@login_required
@user_passes_test(is_librarian)
def manage_categories(request):
    categories = Category.objects.annotate(book_count=Count('books'))
    total_categories = categories.count()
    most_popular_category = categories.order_by('-book_count').first()
    avg_books_per_category = categories.aggregate(avg=Count('books'))['avg'] or 0
    
    context = {
        'categories': categories,
        'total_categories': total_categories,
        'most_popular_category': most_popular_category,
        'avg_books_per_category': avg_books_per_category,
    }
    return render(request, 'librarians/manage_categories.html', context)

@login_required
@user_passes_test(is_librarian)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('librarians:manage_categories')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'librarians/category_form.html', context)

@login_required
@user_passes_test(is_librarian)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('librarians:manage_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'librarians/category_form.html', context)

@login_required
@user_passes_test(is_librarian)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('librarians:manage_categories')
    
    context = {
        'category': category,
    }
    return render(request, 'librarians/confirm_delete_category.html', context)

@login_required
@user_passes_test(is_librarian)
def borrowing_records(request):
    records = BorrowingRecord.objects.all().select_related('book', 'borrower')
    
    # Filtering
    status = request.GET.get('status')
    if status:
        records = records.filter(status=status)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        records = records.filter(
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query) |
            Q(borrower__username__icontains=search_query)
        )
    
    context = {
        'records': records,
        'status': status,
        'search_query': search_query,
    }
    return render(request, 'librarians/borrowing_records.html', context)

@login_required
@user_passes_test(is_librarian)
def manage_fines(request):
    students_with_fines = User.objects.filter(
        role='STUDENT',
        fine_balance__gt=0
    ).order_by('-fine_balance')
    
    context = {
        'students': students_with_fines,
    }
    return render(request, 'librarians/manage_fines.html', context)

@login_required
@user_passes_test(is_librarian)
def update_fine(request, pk):
    student = get_object_or_404(User, pk=pk, role='STUDENT')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        amount = float(request.POST.get('amount', 0))
        
        if action == 'add':
            student.fine_balance += amount
        elif action == 'subtract':
            student.fine_balance = max(0, student.fine_balance - amount)
        
        student.save()
        messages.success(request, 'Fine updated successfully!')
        return redirect('librarians:manage_fines')
    
    context = {
        'student': student,
    }
    return render(request, 'librarians/update_fine.html', context)

@login_required
@user_passes_test(is_librarian)
def search_google_books(request):
    """
    Search for books using Google Books API
    """
    if not request.user.is_authenticated or not request.user.is_librarian:
        return JsonResponse({
            'error': 'Unauthorized',
            'message': 'You must be logged in as a librarian to perform this action.'
        }, status=403)

    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'books': []})
    
    try:
        google_books = GoogleBooksService()
        books = google_books.search_books(query)
        return JsonResponse({'books': books})
    except ValueError as e:
        logger.error(f"Configuration error in search_google_books: {str(e)}")
        return JsonResponse({
            'error': 'Configuration Error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Error in search_google_books: {str(e)}")
        return JsonResponse({
            'error': 'Server Error',
            'message': 'An unexpected error occurred. Please try again later.'
        }, status=500)

@login_required
@user_passes_test(is_librarian)
def import_google_book(request, google_books_id):
    """
    Import book details from Google Books
    """
    google_books = GoogleBooksService()
    book_details = google_books.get_book_details(google_books_id)
    
    if book_details:
        return JsonResponse({
            'success': True,
            'book': book_details
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Book not found'
        })

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # Check if user is a manager
    if not request.user.is_manager:
        messages.error(request, 'Only managers can delete books.')
        return redirect('librarians:manage_books')
    
    # Check if book is currently borrowed
    if BorrowingRecord.objects.filter(book=book, status='BORROWED').exists():
        messages.error(request, 'Cannot delete book that is currently borrowed.')
        return redirect('librarians:manage_books')
    
    # Delete the book
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('librarians:manage_books')

@login_required
@user_passes_test(is_librarian)
def manage_users(request):
    # Get all users with their borrowing counts and fine balances
    users = User.objects.annotate(
        total_borrowings=Count('book_borrowings'),
        active_borrowings=Count('book_borrowings', filter=Q(book_borrowings__status='BORROWED')),
        total_fines=Sum('book_borrowings__fine_amount')
    ).order_by('username')
    
    # Get statistics
    total_users = users.count()
    active_students = users.filter(role='STUDENT', is_active=True).count()
    total_fines = users.aggregate(total=Sum('fine_balance'))['total'] or 0
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_students': active_students,
        'total_fines': total_fines,
    }
    return render(request, 'librarians/manage_users.html', context)

@login_required
@user_passes_test(is_librarian)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Get user's borrowing history
    borrowing_history = BorrowingRecord.objects.filter(
        borrower=user
    ).select_related('book').order_by('-borrowed_date')
    
    # Get current borrowings
    current_borrowings = borrowing_history.filter(status='BORROWED')
    
    # Get fine history
    fine_history = borrowing_history.filter(fine_amount__gt=0)
    
    context = {
        'user': user,
        'borrowing_history': borrowing_history,
        'current_borrowings': current_borrowings,
        'fine_history': fine_history,
    }
    return render(request, 'librarians/user_detail.html', context)

@login_required
@user_passes_test(is_librarian)
def profile(request):
    return render(request, 'librarians/profile.html')

@login_required
def borrowing_report(request):
    if not request.user.role == 'LIBRARIAN':
        return redirect('books:list')
    
    # Get date range from request or use default (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Get borrowing statistics
    total_borrowings = BorrowingRecord.objects.filter(
        borrowed_date__range=[start_date, end_date]
    ).count()
    
    active_borrowings = BorrowingRecord.objects.filter(
        status='BORROWED'
    ).count()
    
    overdue_borrowings = BorrowingRecord.objects.filter(
        status='OVERDUE'
    ).count()
    
    returned_books = BorrowingRecord.objects.filter(
        status='RETURNED',
        return_date__range=[start_date, end_date]
    ).count()
    
    # Get popular books
    popular_books = BorrowingRecord.objects.filter(
        borrowed_date__range=[start_date, end_date]
    ).values('book__title').annotate(
        borrow_count=Count('id')
    ).order_by('-borrow_count')[:5]
    
    context = {
        'total_borrowings': total_borrowings,
        'active_borrowings': active_borrowings,
        'overdue_borrowings': overdue_borrowings,
        'returned_books': returned_books,
        'popular_books': popular_books,
        'start_date': start_date.date(),
        'end_date': end_date.date(),
    }
    
    return render(request, 'librarians/borrowing_report.html', context)
