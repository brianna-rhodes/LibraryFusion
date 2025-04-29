from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def save(self, *args, **kwargs):
        if not self.available_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

class BorrowingRecord(models.Model):
    STATUS_CHOICES = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowing_records')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_borrowings')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BORROWED')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.borrower.username} borrowed {self.book.title}"
    
    class Meta:
        ordering = ['-borrowed_date']

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ORDERED', 'Ordered'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    )
    
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    order_date = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order for {self.quantity} copies of {self.book.title}"
    
    def total_cost(self):
        return self.quantity * self.book.price
    
    class Meta:
        ordering = ['-order_date']
