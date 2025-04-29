from django.db import models
from django.conf import settings
from books.models import Book
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"
    
    def get_rating_display(self):
        return dict(self.RATING_CHOICES)[self.rating]
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'user']
