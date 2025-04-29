from django.urls import path
from . import views

app_name = 'librarians'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.manage_books, name='manage_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('books/search/', views.search_google_books, name='search_google_books'),
    path('books/import/<str:google_books_id>/', views.import_google_book, name='import_google_book'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('borrowing-records/', views.borrowing_records, name='borrowing_records'),
    path('fines/', views.manage_fines, name='manage_fines'),
    path('fines/<int:pk>/update/', views.update_fine, name='update_fine'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
] 