from django.contrib import admin
from catalog.models import Product, Category
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
admin.site.register(Product, ProductAdmin)  
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)    