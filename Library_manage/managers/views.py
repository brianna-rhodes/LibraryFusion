from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta
from account.models import User
from books.models import Book, BorrowingRecord, Category
from .forms import LibrarianForm, SystemSettingsForm, BorrowingSettingsForm, FineSettingsForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from reviews.models import Review
from .models import Fines

def is_manager(user):
    return user.is_authenticated and user.is_manager

@login_required
@user_passes_test(is_manager)
def dashboard(request):
    # Get statistics
    total_books = Book.objects.count()
    total_borrowed = BorrowingRecord.objects.filter(status='BORROWED').count()
    overdue_books = BorrowingRecord.objects.filter(
        status='BORROWED',
        due_date__lt=timezone.now()
    ).count()
    total_librarians = User.objects.filter(role='LIBRARIAN').count()
    
    context = {
        'total_books': total_books,
        'total_borrowed': total_borrowed,
        'overdue_books': overdue_books,
        'total_librarians': total_librarians,
    }
    return render(request, 'managers/dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def manage_librarians(request):
    librarians = User.objects.filter(role='LIBRARIAN')
    return render(request, 'managers/manage_librarians.html', {'librarians': librarians})

@login_required
@user_passes_test(is_manager)
def add_librarian(request):
    if request.method == 'POST':
        form = LibrarianForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_librarian = True
            user.save()
            messages.success(request, 'Librarian added successfully!')
            return redirect('managers:manage_librarians')
    else:
        form = LibrarianForm()
    return render(request, 'managers/librarian_form.html', {'form': form, 'title': 'Add Librarian'})

@login_required
@user_passes_test(is_manager)
def edit_librarian(request, pk):
    librarian = get_object_or_404(User, pk=pk, is_librarian=True)
    if request.method == 'POST':
        form = LibrarianForm(request.POST, instance=librarian)
        if form.is_valid():
            form.save()
            messages.success(request, 'Librarian updated successfully!')
            return redirect('managers:manage_librarians')
    else:
        form = LibrarianForm(instance=librarian)
    return render(request, 'managers/librarian_form.html', {'form': form, 'title': 'Edit Librarian'})

@login_required
@user_passes_test(is_manager)
def delete_librarian(request, pk):
    librarian = get_object_or_404(User, pk=pk, is_librarian=True)
    if request.method == 'POST':
        librarian.delete()
        messages.success(request, 'Librarian deleted successfully!')
        return redirect('managers:manage_librarians')
    return render(request, 'managers/confirm_delete.html', {'object': librarian})

@login_required
@user_passes_test(is_manager)
def system_settings(request):
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            # Save settings logic here
            messages.success(request, 'Settings updated successfully!')
            return redirect('managers:settings')
    else:
        form = SystemSettingsForm()
    return render(request, 'managers/settings.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def borrowing_settings(request):
    if request.method == 'POST':
        form = BorrowingSettingsForm(request.POST)
        if form.is_valid():
            # Save borrowing settings logic here
            messages.success(request, 'Borrowing settings updated successfully!')
            return redirect('managers:borrowing_settings')
    else:
        form = BorrowingSettingsForm()
    return render(request, 'managers/borrowing_settings.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def fine_settings(request):
    if request.method == 'POST':
        form = FineSettingsForm(request.POST)
        if form.is_valid():
            # Save fine settings logic here
            messages.success(request, 'Fine settings updated successfully!')
            return redirect('managers:fine_settings')
    else:
        form = FineSettingsForm()
    return render(request, 'managers/fine_settings.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def borrowing_report(request):
    # Get borrowing statistics
    total_borrowings = BorrowingRecord.objects.count()
    active_borrowings = BorrowingRecord.objects.filter(status='BORROWED').count()
    overdue_borrowings = BorrowingRecord.objects.filter(
        status='BORROWED',
        due_date__lt=timezone.now()
    ).count()
    
    # Get popular books
    popular_books = Book.objects.annotate(
        borrow_count=Count('borrowing_records')
    ).order_by('-borrow_count')[:5]
    
    context = {
        'total_borrowings': total_borrowings,
        'active_borrowings': active_borrowings,
        'overdue_borrowings': overdue_borrowings,
        'popular_books': popular_books,
    }
    return render(request, 'managers/borrowing_report.html', context)

@login_required
@user_passes_test(is_manager)
def fine_report(request):
    # Get fine statistics
    total_fines = BorrowingRecord.objects.aggregate(
        total=Sum('fine_amount')
    )['total'] or 0
    
    unpaid_fines = BorrowingRecord.objects.filter(
        fine_amount__gt=0,
        status__in=['BORROWED', 'OVERDUE']
    ).aggregate(total=Sum('fine_amount'))['total'] or 0
    
    context = {
        'total_fines': total_fines,
        'unpaid_fines': unpaid_fines,
    }
    return render(request, 'managers/fine_report.html', context)

@login_required
@user_passes_test(is_manager)
def inventory_report(request):
    # Get inventory statistics
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available_copies__gt=0).count()
    categories = Book.objects.values('category__name').annotate(
        count=Count('id')
    )
    
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'categories': categories,
    }
    return render(request, 'managers/inventory_report.html', context)

@login_required
@user_passes_test(is_manager)
def manage_users(request):
    users = User.objects.all().prefetch_related('book_borrowings')
    for user in users:
        user.borrowed_count = user.book_borrowings.filter(status='BORROWED').count()
    return render(request, 'managers/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_manager)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    borrowing_history = BorrowingRecord.objects.filter(borrower=user)
    return render(request, 'managers/user_detail.html', {
        'user': user,
        'borrowing_history': borrowing_history
    })

@login_required
@user_passes_test(is_manager)
def suspend_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        action = 'suspended' if not user.is_active else 'activated'
        messages.success(request, f'User {action} successfully!')
        return redirect('managers:user_detail', pk=pk)
    return render(request, 'managers/confirm_suspend.html', {'user': user})

class ReportsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'managers/reports.html'
    context_object_name = 'reports'

    def test_func(self):
        return self.request.user.is_manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Book statistics
        context['total_books'] = Book.objects.count()
        context['books_by_category'] = Category.objects.annotate(book_count=Count('books'))
        context['top_rated_books'] = Book.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')[:5]
        
        # User statistics
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        
        # Review statistics
        context['total_reviews'] = Review.objects.count()
        context['reviews_by_month'] = Review.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Fine statistics using BorrowingRecord
        context['total_fines'] = BorrowingRecord.objects.aggregate(
            total=Sum('fine_amount')
        )['total'] or 0
        context['unpaid_fines'] = BorrowingRecord.objects.filter(
            fine_amount__gt=0,
            status__in=['BORROWED', 'OVERDUE']
        ).aggregate(total=Sum('fine_amount'))['total'] or 0
        
        return context

    def get_queryset(self):
        # Return an empty queryset since we're using context data
        return []
