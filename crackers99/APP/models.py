from django.db import models
import os
from datetime import datetime

def product_image_upload_path(instance, filename):
    extension = os.path.splitext(filename)[-1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{instance.name}_{timestamp}{extension}"
    return os.path.join('product_images', new_filename)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)  # Changed field to BooleanField
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)

