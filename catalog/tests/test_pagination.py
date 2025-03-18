from django.test import TestCase
from django.core.paginator import Paginator
from rest_framework.test import APITestCase
from rest_framework.pagination import PageNumberPagination
from django.urls import reverse
from catalog.models import Category, Product
from decimal import Decimal

class PaginationTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        # Create 15 products for pagination testing
        for i in range(15):
            Product.objects.create(
                name=f'Product {i}',
                description=f'Description {i}',
                price=Decimal(f'{i+10}.99'),
                category=self.category,
                stock_quantity=i+5,
                sku=f'SKU{i}'
            )

    def test_product_pagination(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_product_pagination_second_page(self):
        url = reverse('product-list')
        response = self.client.get(f'{url}?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_invalid_page(self):
        url = reverse('product-list')
        response = self.client.get(f'{url}?page=999')
        self.assertEqual(response.status_code, 404)


class FilterTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product1 = Product.objects.create(
            name='Laptop',
            price=Decimal('999.99'),
            category=self.category,
            stock_quantity=5,
            sku='LAP001'
        )
        self.product2 = Product.objects.create(
            name='Phone',
            price=Decimal('499.99'),
            category=self.category,
            stock_quantity=0,
            sku='PHO001'
        )

    def test_price_filter(self):
        url = reverse('product-list')
        response = self.client.get(f'{url}?min_price=600')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Laptop')

    def test_stock_status_filter(self):
        url = reverse('product-list')
        response = self.client.get(f'{url}?stock_status=out_of_stock')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Phone')

    def test_category_filter(self):
        url = reverse('product-list')
        response = self.client.get(f'{url}?category={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)


class StockManagementTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            price=Decimal('999.99'),
            category=self.category,
            stock_quantity=10,
            sku='LAP001'
        )

    def test_adjust_stock(self):
        url = reverse('product-adjust-stock', kwargs={'pk': self.product.pk})
        response = self.client.post(url, {'adjustment': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['new_stock_quantity'], 15)

    def test_prevent_negative_stock(self):
        url = reverse('product-adjust-stock', kwargs={'pk': self.product.pk})
        response = self.client.post(url, {'adjustment': -15})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

    def test_stock_history_creation(self):
        url = reverse('product-adjust-stock', kwargs={'pk': self.product.pk})
        self.client.post(url, {'adjustment': 5})
        history = self.product.stock_history.first()
        self.assertEqual(history.quantity_changed, 5)
        self.assertEqual(history.previous_quantity, 10)
        self.assertEqual(history.new_quantity, 15)


class PerformanceTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        # Create 100 products for performance testing
        for i in range(100):
            Product.objects.create(
                name=f'Product {i}',
                price=Decimal(f'{i+10}.99'),
                category=self.category,
                stock_quantity=i,
                sku=f'SKU{i}'
            )

    def test_query_performance(self):
        url = reverse('product-list')
        with self.assertNumQueries(2):  # Should only need 2 queries with select_related
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_index_effectiveness(self):
        # Test querying using indexed fields
        Product.objects.filter(name='Product 1').exists()
        Product.objects.filter(sku='SKU1').exists()
        Product.objects.filter(category=self.category).exists()
        Product.objects.filter(stock_quantity=0).exists()