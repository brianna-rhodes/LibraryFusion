from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(choices=Review.RATING_CHOICES),
            'review_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts about this book...'
            }),
        }
        labels = {
            'rating': 'Your Rating',
            'review_text': 'Your Review',
        } 