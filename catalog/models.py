from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Index

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return str(self.name)  


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['stock_quantity']),
        ]
        ordering = ['name']

    def adjust_stock(self, quantity, reason="Manual adjustment"):
        previous_quantity = self.stock_quantity
        new_quantity = previous_quantity + quantity
        
        if new_quantity < 0:
            raise ValueError("Stock cannot be negative")
            
        self.stock_quantity = new_quantity
        self.save()
        
        # Create stock history record
        StockHistory.objects.create(
            product=self,
            quantity_changed=quantity,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            change_reason=reason
        )
        
        # Check for low stock alert
        if self.stock_quantity <= 5:
            self.send_low_stock_alert()

    def send_low_stock_alert(self):
        # In a real application, you might want to:
        # 1. Send email
        # 2. Create notification
        # 3. Trigger webhook
        # For now, we'll just print
        print(f"Low stock alert: {self.name} - {self.stock_quantity} units remaining")

    def __str__(self):
        return self.name


class StockHistory(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='stock_history'
    )
    quantity_changed = models.IntegerField()
    previous_quantity = models.PositiveIntegerField()
    new_quantity = models.PositiveIntegerField()
    change_reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            Index(fields=['product', '-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.quantity_changed} units"
