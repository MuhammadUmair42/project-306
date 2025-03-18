from django.db import models
from django.core.validators import MinValueValidator
from .category import Category

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
        ordering = ['name']

    def __str__(self):
        return self.name

    def adjust_stock(self, quantity):
        """
        Adjust stock quantity. Positive number increases stock,
        negative number decreases stock.
        """
        new_quantity = self.stock_quantity + quantity
        if new_quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.stock_quantity = new_quantity
        self.save()