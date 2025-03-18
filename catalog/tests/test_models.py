from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from catalog.models import Category, Product

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Electronic items')
        self.assertTrue(self.category.created_at)
        self.assertTrue(self.category.updated_at)

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Electronics')

    def test_unique_category_name(self):
        with self.assertRaises(ValidationError):
            duplicate_category = Category(
                name='Electronics',
                description='Duplicate category'
            )
            duplicate_category.full_clean()


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=Decimal('999.99'),
            category=self.category,
            stock_quantity=10,
            sku='LAP001'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertEqual(self.product.price, Decimal('999.99'))
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.stock_quantity, 10)
        self.assertEqual(self.product.sku, 'LAP001')

    def test_product_str_representation(self):
        self.assertEqual(str(self.product), 'Laptop')

    def test_unique_sku(self):
        with self.assertRaises(ValidationError):
            duplicate_product = Product(
                name='Another Laptop',
                price=Decimal('899.99'),
                category=self.category,
                stock_quantity=5,
                sku='LAP001'
            )
            duplicate_product.full_clean()

    def test_negative_price_validation(self):
        with self.assertRaises(ValidationError):
            product = Product(
                name='Test Product',
                price=Decimal('-10.00'),
                category=self.category,
                stock_quantity=5,
                sku='TEST001'
            )
            product.full_clean()

    def test_adjust_stock(self):
        # Test increasing stock
        self.product.adjust_stock(5)
        self.assertEqual(self.product.stock_quantity, 15)

        # Test decreasing stock
        self.product.adjust_stock(-3)
        self.assertEqual(self.product.stock_quantity, 12)

        # Test negative stock prevention
        with self.assertRaises(ValueError):
            self.product.adjust_stock(-20)