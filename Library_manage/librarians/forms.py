from django import forms
from books.models import Book, Category, BorrowingRecord
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone

class BorrowingRecordForm(forms.ModelForm):
    class Meta:
        model = BorrowingRecord
        fields = ['book', 'borrower', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=BorrowingRecord.STATUS_CHOICES),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'category', 'description',
            'total_copies', 'available_copies', 'cover_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'total_copies': forms.NumberInput(attrs={'min': 0}),
            'available_copies': forms.NumberInput(attrs={'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        total_copies = cleaned_data.get('total_copies')
        available_copies = cleaned_data.get('available_copies')
        
        if total_copies is not None and available_copies is not None:
            if available_copies > total_copies:
                raise forms.ValidationError(
                    "Available copies cannot be greater than total copies."
                )
        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FineForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    ) 
