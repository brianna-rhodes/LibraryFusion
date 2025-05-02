from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/password/', PasswordChangeView.as_view(template_name='account/password_change.html', success_url='done/'), name='password_change'),
    path('profile/password/done/', PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
] 
