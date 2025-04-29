from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('book/<int:book_id>/add/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('book/<int:book_id>/reviews/', views.book_reviews, name='book_reviews'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('top-rated/', views.top_rated_books, name='top_rated'),
] 