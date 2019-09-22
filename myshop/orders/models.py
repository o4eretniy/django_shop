from django.db import models
from shop.models import Product
from cupons.models import Cupon
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Order(models.Model):
    first_name = models.CharField(verbose_name='Name', max_length=50)
    last_name = models.CharField(verbose_name='Surname', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=100)
    address = models.CharField(verbose_name='Address', max_length=250)
    postal_code = models.CharField(verbose_name='Postal code', max_length=20)
    city = models.CharField(verbose_name='City', max_length=100)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    paid = models.BooleanField(verbose_name='Paid', default=True)
    cupon = models.ForeignKey(Cupon, related_name='orders', null=True, blank=True,
                                                          on_delete=models.PROTECT)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(100)])

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order: {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=1)

    def __str__(self):
        return '{}'.format(self.id)
    
    def get_cost(self):
        return self.price * self.quantity