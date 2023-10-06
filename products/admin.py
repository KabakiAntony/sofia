from django.contrib import admin
from sofia.admin import sofia_admin_site
from .models import Product, Category, Image, GoesWellWith, Product_Entry, Color, Size


class ProductEntryInline(admin.TabularInline):
    model = Product_Entry


class GoesWellWithInline(admin.TabularInline):
    model = GoesWellWith
    fk_name = "product_one"


class ImageInline(admin.TabularInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_display_links = ['title']
    list_filter = ['category']
    inlines = [GoesWellWithInline]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['product_entry', 'thumb']
    readonly_fields = ['thumb']
    list_display_links = ['product_entry']
    list_filter = ['product_entry']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_display_links = ['title']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_display_links = ['name']


class ProductEntryAdmin(admin.ModelAdmin):
    list_display = ['sku', 'title', 'product', 'size',
                    'color', 'quantity', 'price', 'available']
    list_display_links = ['title']
    list_filter = ['product', 'available']
    inlines = [ImageInline]


sofia_admin_site.register(Product, ProductAdmin)
sofia_admin_site.register(Product_Entry, ProductEntryAdmin)
sofia_admin_site.register(Image, ImageAdmin)
sofia_admin_site.register(Category, CategoryAdmin)
sofia_admin_site.register(GoesWellWith)
sofia_admin_site.register(Color, ColorAdmin)
sofia_admin_site.register(Size)
