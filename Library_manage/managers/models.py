from django.db import models
from django.conf import settings
from books.models import BorrowingRecord, Book
from account.models import User
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

class Analytics(models.Model):
    date = models.DateField(auto_now_add=True)
    most_borrowed_books = models.JSONField(default=dict)
    inventory_levels = models.JSONField(default=dict)
    late_returns = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "Analytics"

class Budget(models.Model):
    year = models.IntegerField()
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_replacements = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Budget {self.year}"

class SystemSettings(models.Model):
    review_system_enabled = models.BooleanField(default=True)
    google_books_api_enabled = models.BooleanField(default=False)
    last_backup = models.DateTimeField(null=True, blank=True)
    maintenance_scheduled = models.DateTimeField(null=True, blank=True)
    maintenance_message = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "System Settings"

    def __str__(self):
        return "System Settings"

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    permissions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
