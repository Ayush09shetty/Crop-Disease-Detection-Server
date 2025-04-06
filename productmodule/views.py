import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product
from .serializers import ProductSerializer

# Handle uploaded image and return path
def handle_uploaded_file(file):
    upload_base = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]
    upload_dir = os.path.join(upload_base, 'product_images')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return f"/static/product_images/{file.name}"


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any since we're not authenticating here
@parser_classes([MultiPartParser, FormParser])
def add_product(request):
    image_paths = []
    for file_key in request.FILES:
        file = request.FILES[file_key]
        image_path = handle_uploaded_file(file)
        image_paths.append(image_path)

    data = request.data.copy()
    data['image_paths'] = ",".join(image_paths)

    # Now pass the seller from request.data directly
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Product added successfully",
            "product": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    image_paths = []
    if request.FILES:
        for file_key in request.FILES:
            file = request.FILES[file_key]
            image_path = handle_uploaded_file(file)
            image_paths.append(image_path)
        request.data._mutable = True
        request.data['image_paths'] = ",".join(image_paths)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_by_id(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_by_category(request, category):
    products = Product.objects.filter(category__iexact=category)
    if not products.exists():
        return Response({"error": f"No products found in category: {category}"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)