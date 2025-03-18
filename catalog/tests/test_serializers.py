from decimal import Decimal
from django.test import TestCase
from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer

class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category_data = {
            'name': 'Electronics',
            'description': 'Electronic items'
        }
        self.category = Category.objects.create(**self.category_data)
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), 
                        {'id', 'name', 'description', 'created_at', 'updated_at'})

    def test_name_field_validation(self):
        serializer = CategorySerializer(data=self.category_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'name'})


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product_data = {
            'name': 'Laptop',
            'description': 'High-performance laptop',
            'price': '999.99',
            'category': self.category.id,
            'stock_quantity': 10,
            'sku': 'LAP001'
        }
        self.product = Product.objects.create(**{
            **self.product_data,
            'category': self.category
        })
        self.serializer = ProductSerializer(instance=self.product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            'id', 'name', 'description', 'price', 'category',
            'category_name', 'stock_quantity', 'sku', 'created_at', 'updated_at'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_stock_quantity_validation(self):
        invalid_data = self.product_data.copy()
        invalid_data['stock_quantity'] = -1
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('stock_quantity', serializer.errors)