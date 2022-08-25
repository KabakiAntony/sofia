from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField()
    description = models.CharField(max_length=150, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumb = models.ImageField(default='default.jpeg', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def snippet(self):
        return self.description[:20] + " ..."

