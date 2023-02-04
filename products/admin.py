from django.contrib import admin
from journaling.admin import journaling_admin_site
from .models import Product, Category, Image, GoesWellWith, Product_Entry, Color, Size


class ProductEntryInline(admin.TabularInline):
    model =  Product_Entry


class GoesWellWithInline(admin.TabularInline):
    model = GoesWellWith
    fk_name = "product_one"


class ImageInline(admin.TabularInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category']
    list_display_links = ['title']
    list_filter = ['category']
    inlines = [GoesWellWithInline]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['product_entry','thumb']
    readonly_fields = ['thumb']
    list_display_links = ['product_entry']
    list_filter = ['product_entry']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','description']
    list_display_links = ['title']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code']
    list_display_links = ['name']


class ProductEntryAdmin(admin.ModelAdmin):
    list_display = ['sku', 'title', 'product', 'size', 'color', 'quantity', 'price', 'available']
    list_display_links = ['title']
    list_filter = ['product', 'available']
    inlines = [ImageInline]


journaling_admin_site.register(Product,ProductAdmin)
journaling_admin_site.register(Product_Entry, ProductEntryAdmin)
journaling_admin_site.register(Image,ImageAdmin)
journaling_admin_site.register(Category, CategoryAdmin)
journaling_admin_site.register(GoesWellWith)
journaling_admin_site.register(Color, ColorAdmin)
journaling_admin_site.register(Size)