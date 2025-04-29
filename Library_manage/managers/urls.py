from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    # Dashboard and Overview
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    # Librarian Management
    path('librarians/', views.manage_librarians, name='manage_librarians'),
    path('librarians/add/', views.add_librarian, name='add_librarian'),
    path('librarians/<int:pk>/edit/', views.edit_librarian, name='edit_librarian'),
    path('librarians/<int:pk>/delete/', views.delete_librarian, name='delete_librarian'),
    
    # System Settings
    path('settings/', views.system_settings, name='settings'),
    path('settings/borrowing/', views.borrowing_settings, name='borrowing_settings'),
    path('settings/fines/', views.fine_settings, name='fine_settings'),
    
    # Reports and Analytics
    path('reports/borrowing/', views.borrowing_report, name='borrowing_report'),
    path('reports/fines/', views.fine_report, name='fine_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    
    # User Management
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/suspend/', views.suspend_user, name='suspend_user'),
] 