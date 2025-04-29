from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    ROLES = (
        ('STUDENT', 'Student'),
        ('LIBRARIAN', 'Librarian'),
        ('MANAGER', 'Manager'),
    )
    
    role = models.CharField(max_length=10, choices=ROLES, default='STUDENT')
    is_active = models.BooleanField(default=True)
    fine_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True,
        null=True
    )
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def is_librarian(self):
        return self.role == 'LIBRARIAN'
    
    @property
    def is_manager(self):
        return self.role == 'MANAGER'
    
    @property
    def is_student(self):
        return self.role == 'STUDENT'

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('ONLINE', 'Online'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payments')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Payment of ${self.amount} by {self.user.get_full_name()} on {self.payment_date.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        # Update user's fine balance when payment is made
        if not self.pk:  # Only on creation
            self.user.fine_balance = max(0, self.user.fine_balance - self.amount)
            self.user.save()
        super().save(*args, **kwargs)

class UserNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Note for {self.user.get_full_name()} by {self.created_by.get_full_name()}"
