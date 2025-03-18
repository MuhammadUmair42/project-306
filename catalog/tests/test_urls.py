from django.test import TestCase
from django.urls import reverse, resolve
from catalog.views.category_views import CategoryViewSet
from catalog.views.product_views import ProductViewSet

class UrlTests(TestCase):
    def test_category_list_url(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).func.cls, CategoryViewSet)

    def test_product_list_url(self):
        url = reverse('product-list')
        self.assertEqual(resolve(url).func.cls, ProductViewSet)

    def test_category_detail_url(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, CategoryViewSet)

    def test_product_detail_url(self):
        url = reverse('product-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, ProductViewSet)