from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from catalog.models.category import Category
from catalog.models.product import Product

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_category_list_view(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_list_view(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_filter_by_category(self):
        response = self.client.get(
            f"{reverse('product-list')}?category={self.category.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_stock_adjustment(self):
        url = reverse('product-adjust-stock', kwargs={'pk': self.product.id})
        response = self.client.post(url, {'adjustment': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 15)