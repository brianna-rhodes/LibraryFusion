from django.db import models
from django.conf import settings
from books.models import BorrowingRecord
from django.utils import timezone

# Create your models here.

class Fines(models.Model):
    borrowing_record = models.ForeignKey(
        BorrowingRecord, 
        on_delete=models.CASCADE, 
        related_name='fines',
        help_text="The borrowing record this fine is associated with"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00,
        help_text="The amount of the fine"
    )
    reason = models.TextField(
        help_text="The reason for issuing this fine"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this fine was created"
    )
    paid = models.BooleanField(
        default=False,
        help_text="Whether this fine has been paid"
    )
    paid_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When this fine was paid"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_fines',
        help_text="The user who created this fine"
    )

    class Meta:
        app_label = 'managers'
        verbose_name = 'Fine'
        verbose_name_plural = 'Fines'
        ordering = ['-created_at']

    def __str__(self):
        return f"Fine of ${self.amount} for {self.borrowing_record.book.title}"

    def mark_as_paid(self):
        self.paid = True
        self.paid_at = timezone.now()
        self.save()
