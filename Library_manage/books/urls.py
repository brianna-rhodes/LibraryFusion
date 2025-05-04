from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.book_list, name='list'),
    path('book/<int:pk>/', views.book_detail, name='detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow'),
    path('book/<int:pk>/return/', views.return_book, name='return'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete'),
    path('my-books/', views.my_books, name='my_books'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('add/', views.add_book, name='add'),
    path('import-google-book/<str:google_books_id>/', views.import_google_book, name='import_google_book'),
] 
