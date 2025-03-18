from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from catalog.views import CategoryViewSet, ProductViewSet

class UrlPatternsTest(APITestCase):
    def test_category_list_url(self):
        url = reverse('category-list')
        self.assertEqual(url, '/api/categories/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, CategoryViewSet)

    def test_category_detail_url(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/api/categories/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, CategoryViewSet)

    def test_product_list_url(self):
        url = reverse('product-list')
        self.assertEqual(url, '/api/products/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ProductViewSet)

    def test_product_detail_url(self):
        url = reverse('product-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/api/products/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ProductViewSet)

    def test_product_adjust_stock_url(self):
        url = reverse('product-adjust-stock', kwargs={'pk': 1})
        self.assertEqual(url, '/api/products/1/adjust-stock/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ProductViewSet)

class ApiRootTest(APITestCase):
    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.data)
        self.assertIn('products', response.data)

    def test_api_docs(self):
        response = self.client.get('/docs/')
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirects to login