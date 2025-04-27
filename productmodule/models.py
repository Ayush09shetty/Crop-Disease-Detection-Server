
import uuid
from django.db import models
 

def product_image_upload_path(instance, filename):
    return f"static/product_images/{uuid.uuid4()}_{filename}"

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.UUIDField()
    
    name = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=20)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    about_company_line1 = models.CharField(max_length=500)
    about_company_line2 = models.CharField(max_length=500, null=True, blank=True)
    about_company_line3 = models.CharField(max_length=500, null=True, blank=True)

    about_product_line1 = models.CharField(max_length=500)
    about_product_line2 = models.CharField(max_length=500, null=True, blank=True)
    about_product_line3 = models.CharField(max_length=500, null=True, blank=True)
    about_product_line4 = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/product_images/')

class OrderStatus(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField("Checkout.OrderHistory", on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id} - {self.status}"
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    inventory = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} in stock"