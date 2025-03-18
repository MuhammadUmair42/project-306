from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Category, Product

class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )
        self.list_url = reverse('category-list')
        self.detail_url = reverse('category-detail', kwargs={'pk': self.category.pk})

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_category(self):
        data = {'name': 'Books', 'description': 'Book items'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_search_category(self):
        response = self.client.get(f'{self.list_url}?search=Electronics')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=Decimal('999.99'),
            category=self.category,
            stock_quantity=10,
            sku='LAP001'
        )
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        self.adjust_stock_url = reverse('product-adjust-stock', kwargs={'pk': self.product.pk})

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_category(self):
        response = self.client.get(f'{self.list_url}?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_price_range(self):
        response = self.client.get(f'{self.list_url}?min_price=900&max_price=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_stock_status(self):
        response = self.client.get(f'{self.list_url}?stock_status=in_stock')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_adjust_stock(self):
        data = {'adjustment': 5}
        response = self.client.post(self.adjust_stock_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_stock_quantity'], 15)

    def test_adjust_stock_negative(self):
        data = {'adjustment': -20}
        response = self.client.post(self.adjust_stock_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)