from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.book_list, name='list'),
    path('book/<int:pk>/', views.book_detail, name='detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow'),
    path('my-books/', views.my_books, name='my_books'),
    path('return/<int:pk>/', views.return_book, name='return'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
] 