from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User
from django.core.validators import MinValueValidator
from .models import SystemSettings

class LibrarianForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'required': True}),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }

class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ['review_system_enabled', 'google_books_api_enabled', 'maintenance_scheduled', 'maintenance_message']
        widgets = {
            'maintenance_message': forms.Textarea(attrs={'rows': 3}),
            'maintenance_scheduled': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BorrowingSettingsForm(forms.Form):
    borrowing_period = forms.IntegerField(
        label='Borrowing Period (days)',
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'min': 1})
    )
    renewal_period = forms.IntegerField(
        label='Renewal Period (days)',
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'min': 1})
    )
    max_renewals = forms.IntegerField(
        label='Maximum Renewals',
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'min': 0})
    )
    reservation_period = forms.IntegerField(
        label='Reservation Period (days)',
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'min': 1})
    )

class FineSettingsForm(forms.Form):
    daily_fine = forms.DecimalField(
        label='Daily Fine Amount ($)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    )
    max_fine = forms.DecimalField(
        label='Maximum Fine Amount ($)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    )
    grace_period = forms.IntegerField(
        label='Grace Period (days)',
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'min': 0})
    )
    lost_book_fine = forms.DecimalField(
        label='Lost Book Fine ($)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    ) 
