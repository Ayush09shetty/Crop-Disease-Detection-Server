# import uuid
# from django.db import models

# def product_image_upload_path(instance, filename):
#     return f"static/product_images/{uuid.uuid4()}_{filename}"

# class Product(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     # Seller is now just a UUID (no relation)
#     seller = models.UUIDField()

#     name = models.CharField(max_length=50)
#     brand_name = models.CharField(max_length=50)
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)
#     category = models.CharField(max_length=20)
#     cost_price = models.DecimalField(max_digits=10, decimal_places=2)
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)

#     image_paths = models.TextField(null=True, blank=True)

#     # About company
#     about_company_line1 = models.CharField(max_length=500)
#     about_company_line2 = models.CharField(max_length=500, null=True, blank=True)
#     about_company_line3 = models.CharField(max_length=500, null=True, blank=True)

#     # About product
#     about_product_line1 = models.CharField(max_length=500)
#     about_product_line2 = models.CharField(max_length=500, null=True, blank=True)
#     about_product_line3 = models.CharField(max_length=500, null=True, blank=True)
#     about_product_line4 = models.CharField(max_length=500, null=True, blank=True)

#     def __str__(self):
#         return self.name
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

    # quantity = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# class ProductImage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=product_image_upload_path)

#     def __str__(self):
#         return f"{self.product.name} - {self.image.url}"
class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/product_images/')
