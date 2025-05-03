from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    # Root path - redirect to home
    path('', views.home, name='home'),
    
    # Dashboard and Overview
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    
    # System Settings
    path('settings/', views.system_settings, name='settings'),
    
    # Borrowing Management
    path('borrowing/report/', views.borrowing_report, name='borrowing_report'),
    path('borrowing/settings/', views.borrowing_settings, name='borrowing_settings'),
    path('fines/report/', views.fine_report, name='fine_report'),
    path('fines/settings/', views.fine_settings, name='fine_settings'),
    
    # Librarian Management
    path('librarians/', views.manage_librarians, name='manage_librarians'),
    path('librarians/add/', views.add_librarian, name='add_librarian'),
    path('librarians/<int:pk>/edit/', views.edit_librarian, name='edit_librarian'),
    path('librarians/<int:pk>/delete/', views.delete_librarian, name='delete_librarian'),
    
    # User Management
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/suspend/', views.suspend_user, name='suspend_user'),
    path('users/<int:pk>/confirm-suspend/', views.confirm_suspend, name='confirm_suspend'),

    # Admin Panel
    path('admin-panel/', views.admin_control_panel, name='admin_panel'),
    path('toggle-feature/', views.toggle_feature, name='toggle_feature'),
    path('export-report/<str:report_type>/', views.export_report, name='export_report'),
    path('manage-roles/', views.manage_user_roles, name='manage_roles'),
    path('update-settings/', views.update_system_settings, name='update_settings'),
    path('update-role/', views.update_user_role, name='update_role'),
] 
