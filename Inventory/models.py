from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_products',
        null=True,
        blank=True,
        editable=False,
    )
    product_id = models.CharField()
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    qty = models.IntegerField()

    @property
    def total_amount(self):
        return self.price * self.qty

    def __str__(self):
        return self.name
