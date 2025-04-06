from django.shortcuts import render
import os
import random
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

@api_view(['GET'])
@permission_classes([AllowAny])
def get_random_hero_images(request):
    folder_path = os.path.join(settings.STATICFILES_DIRS[0], 'heroimages')
    try:
        all_images = os.listdir(folder_path)  
        random_images = random.sample(all_images, min(4, len(all_images)))  
        image_urls = [request.build_absolute_uri(f"{settings.STATIC_URL}heroimages/{img}") for img in random_images]  
        return Response({"images": image_urls}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['PUT'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser]) 
def upload_hero_image(request):    
    image = request.FILES.get('image')
    image_name = request.data.get('image_name')

    if not image or not image_name:
        return Response({"error": "Image and image_name are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the heroimages folder exists
    upload_folder = os.path.join(settings.STATICFILES_DIRS[0], 'heroimages')
    os.makedirs(upload_folder, exist_ok=True)

    # Save the file, replacing an existing one if needed
    file_path = os.path.join(upload_folder, image_name)

    with open(file_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return Response({"message": "Image uploaded successfully", "image_name": image_name}, status=status.HTTP_200_OK)
