from rest_framework import serializers
from .models import Product

# class ProductSerializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(allow_empty_file=False, use_url=False),
#         write_only=True,
#         required=False
#     )
    
#     class Meta:
#         model = Product
#         fields = '__all__'
#         extra_kwargs = {'seller': {'required': False}}  # Seller is assigned automatically
    
#     def create(self, validated_data):
#         request = self.context.get('request')
#         if request and hasattr(request, 'user'):
#             validated_data['seller'] = request.user  # Assign authenticated user
        
#         images = validated_data.pop('images', [])  # Extract images from request
#         product_instance = Product.objects.create(**validated_data)
        
#         image_paths = []
#         for image in images[:5]:  # Limit to 5 images
#             image_path = self.save_image(image)
#             if image_path:
#                 image_paths.append(image_path)
        
#         product_instance.image_paths = ",".join(image_paths)  # Store paths
#         product_instance.save()
#         return product_instance
    
#     def update(self, instance, validated_data):
#         images = validated_data.pop('images', [])
#         image_paths = []
        
#         for image in images[:5]:
#             image_path = self.save_image(image)
#             if image_path:
#                 image_paths.append(image_path)
        
#         if image_paths:
#             instance.image_paths = ",".join(image_paths)
        
#         return super().update(instance, validated_data)
    
#     def save_image(self, image):
#         """Save image to static/product_images/"""
#         import os
#         from django.conf import settings
#         from PIL import Image
        
#         try:
#             save_dir = os.path.join(settings.BASE_DIR, "static", "product_images")
#             os.makedirs(save_dir, exist_ok=True)
            
#             filename = os.path.splitext(image.name)[0]
#             new_filename = f"{filename}.png"
#             save_path = os.path.join(save_dir, new_filename)
            
#             with Image.open(image) as img:
#                 img = img.convert("RGBA")
#                 img.save(save_path, "PNG")
            
#             return f"/static/product_images/{new_filename}"
#         except Exception as e:
#             print(f"Error saving image: {str(e)}")
#             return None
# Updated ProductSerializer (if using view to handle image saving)
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#         extra_kwargs = {'seller': {'required': False}}
from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class ProductSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        uploaded_images = self.context['request'].FILES.getlist('uploaded_images')
        validated_data.pop('uploaded_images', None)  # Prevent unknown field error

        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product

