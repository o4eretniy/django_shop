from django.db import models
from django.urls import reverse

# Create your models here.

# Category model
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:ProductListByCategory", args=[self.slug])

# Product model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
        verbose_name='Category', on_delete=models.PROTECT)
    name = models.CharField(max_length=200, db_index=True,
        verbose_name='Name')
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, 
        verbose_name='Item Image')
    description = models.TextField(blank=True, verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    stock = models.PositiveIntegerField(verbose_name='In stock')
    available = models.BooleanField(default=True, verbose_name='Available')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:ProductDetail", args=[self.id, self.slug])