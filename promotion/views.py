# This view is used to show the promotion images and to add the promotion images by the seller
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .utils import save_promotion_image
import os
import random
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


# This function is used to upload the promotion image
@api_view(['PUT'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser]) 
def upload_promotion_image(request):    
    image = request.FILES.get('image')
    image_name = request.data.get('image_name')
    if not image or not image_name:
        return Response({"error": "Image and image_name are required"}, status=status.HTTP_400_BAD_REQUEST)
    saved_image_name = save_promotion_image(image, image_name)
    return Response({"message": "Image uploaded successfully", "image_name": saved_image_name}, status=status.HTTP_200_OK)


#This function is used to randomly get one promotion image
@api_view(['GET'])
@permission_classes([AllowAny])
def get_random_promotion_image_path(request):
    promotion_dir = os.path.join(settings.BASE_DIR, 'static/promotion')
    if not os.path.exists(promotion_dir):
        return Response({"error": "No directory not found"}, status=status.HTTP_404_NOT_FOUND)
    image_files = [f for f in os.listdir(promotion_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        return Response({"error": "No images found in promotion directory"}, status=status.HTTP_404_NOT_FOUND)
    random_image = random.choice(image_files)
    image_url = f"{settings.STATIC_URL}promotion/{random_image}"
    return Response({"image_url": request.build_absolute_uri(image_url)}, status=status.HTTP_200_OK)