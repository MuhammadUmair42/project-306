from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from catalog.models.category import Category
from catalog.models.product import Product
from catalog.admin import CategoryAdmin, ProductAdmin

class MockRequest:
    pass

class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password123'
        )
        self.client.force_login(self.admin_user)
        
        # Create test data
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=99.99,
            category=self.category,
            stock_quantity=10,
            sku='TEST123'
        )

    def test_category_admin_display(self):
        category_admin = CategoryAdmin(Category, self.site)
        self.assertEqual(list(category_admin.list_display), 
                        ['name', 'created_at', 'updated_at'])

    def test_product_admin_display(self):
        product_admin = ProductAdmin(Product, self.site)
        self.assertEqual(list(product_admin.list_display),
                        ['name', 'category', 'price', 'stock_quantity', 'created_at'])