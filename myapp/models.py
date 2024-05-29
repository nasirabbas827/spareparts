from django.db import models
from django.contrib.auth.models import User

# Model to represent the category of spare parts
class SparePartCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Model to represent a spare part
class SparePart(models.Model):
    category = models.ForeignKey(SparePartCategory, on_delete=models.CASCADE, related_name='spare_parts')
    name = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Selling price
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='spare_parts/', blank=True, null=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Purchase(models.Model):
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)


   