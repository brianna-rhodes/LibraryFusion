from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from books.models import Book
from .models import Review
from .forms import ReviewForm

# Create your views here.

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if user has already reviewed this book
    existing_review = Review.objects.filter(book=book, user=request.user).first()
    if existing_review:
        messages.warning(request, 'You have already reviewed this book.')
        return redirect('books:detail', pk=book_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('books:detail', pk=book_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'book': book
    })

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('books:detail', pk=review.book.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted successfully!')
        return redirect('books:detail', pk=book_id)
    
    return render(request, 'reviews/confirm_delete.html', {'review': review})

def book_reviews(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book).select_related('user')
    
    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_count = reviews.count()
    
    # Get rating distribution
    rating_distribution = reviews.values('rating').annotate(
        count=Count('id')
    ).order_by('rating')
    
    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'rating_count': rating_count,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'reviews/book_reviews.html', context)

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related('book')
    return render(request, 'reviews/my_reviews.html', {'reviews': reviews})

def top_rated_books(request):
    # Get books with at least 5 reviews and order by average rating
    books = Book.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).filter(
        review_count__gte=5
    ).order_by('-avg_rating')[:10]
    
    return render(request, 'reviews/top_rated_books.html', {'books': books})
