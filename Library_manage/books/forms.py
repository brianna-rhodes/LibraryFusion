from django import forms
from .models import Book, Category, BorrowingRecord, Order, BookRequest

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'category', 'cover_image', 'total_copies', 'published_date']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BookSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or ISBN...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowingRecord
        fields = []  # No fields needed as we set them in the view 

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'quantity', 'estimated_delivery', 'notes']
        widgets = {
            'estimated_delivery': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.all().order_by('title') 

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['title', 'author']
