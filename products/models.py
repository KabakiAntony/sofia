import uuid
import secrets
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def short_name(self):
        return self.title[:15]

    def snippet(self):
        return self.description[:20] + " ..."

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            random_url = secrets.token_hex(8)
            joined_string = "-".join([self.title,random_url])
            self.slug = slugify(joined_string)
        super(Product, self).save(*args, **kwargs)
        

    class Meta:
        verbose_name_plural = "Products"


class GoesWellWith(models.Model):
    product_one = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="following")
    product_two = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.product_one.title} Goes well with -> {self.product_two.title}"

    class Meta:
        verbose_name_plural = "Products it goes well with"


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Colors"


class Size(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Sizes"


class Product_Entry(models.Model):
    sku = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(unique=True, max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Product Entries"


class Image(models.Model):
    product_entry = models.ForeignKey(Product_Entry, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True)
    thumb = models.ImageField(default='default.jpeg', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Images"



    



