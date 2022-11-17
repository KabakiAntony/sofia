from django.contrib import admin
from journaling.admin import journaling_admin_site
from .models import Product, Category, ProductImage, GoesWellWith


class GoesWellWithInline(admin.TabularInline):
    model = GoesWellWith
    fk_name = "product_one"


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    # define how the custom form is going to be rendered
    list_display = ['id','name','description','category','price', 'stock', 'available', 'date']
    list_display_links = ['name']
    list_filter = ['category']
    inlines = [ProductImageInline, GoesWellWithInline]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id','product','thumb']
    readonly_fields = ['thumb']
    list_display_links = ['product']
    list_filter = ['product']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','description']
    list_display_links = ['name']

journaling_admin_site.register(Product,ProductAdmin)
journaling_admin_site.register(ProductImage,ProductImageAdmin)
journaling_admin_site.register(Category, CategoryAdmin)
journaling_admin_site.register(GoesWellWith)
