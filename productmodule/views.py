import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, ProductImage
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderStatus
from .serializers import OrderStatusSerializer

# Handle uploaded image and return path
# def handle_uploaded_file(file):
#     upload_base = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]
#     upload_dir = os.path.join(upload_base, 'product_images')
#     os.makedirs(upload_dir, exist_ok=True)
#     file_path = os.path.join(upload_dir, file.name)
#     with open(file_path, 'wb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)
#     return f"/static/product_images/{file.name}"

import os
from django.conf import settings

def handle_uploaded_file(file):
    upload_base = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]
    upload_dir = os.path.join(upload_base, 'product_images')
    os.makedirs(upload_dir, exist_ok=True)

    # Generate a unique filename to avoid conflicts
    from uuid import uuid4
    filename = f"{uuid4().hex}_{file.name}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Construct a URL path (e.g., /static/product_images/filename.jpg)
    return f"/static/product_images/{filename}"

# views.py
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def add_product(request):
    serializer = ProductSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        product = serializer.save()
        return Response({
            "message": "Product added successfully",
            "product": ProductSerializer(product).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['POST'])
# @permission_classes([AllowAny])  # Allow any since we're not authenticating here
# @parser_classes([MultiPartParser, FormParser])
# def add_product(request):
#     image_paths = []
#     for file_key in request.FILES:
#         file = request.FILES[file_key]
#         image_path = handle_uploaded_file(file)
#         image_paths.append(image_path)

#     data = request.data.copy()
#     data['image_paths'] = ",".join(image_paths)

#     # Now pass the seller from request.data directly
#     serializer = ProductSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({
#             "message": "Product added successfully",
#             "product": serializer.data
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def list_products(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Save uploaded images (if any)
    uploaded_images = request.FILES.getlist('uploaded_images')
    if uploaded_images:
        for image in uploaded_images:
            filename = f"{uuid.uuid4()}_{image.name}"
            save_path = os.path.join(settings.BASE_DIR, 'static', 'product_images', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Save to ProductImage model
            ProductImage.objects.create(
                id=uuid.uuid4(),
                product=product,
                image=f"/static/product_images/{filename}"
            )

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_product_by_id(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_products_by_category(request, category):
#     products = Product.objects.filter(category__iexact=category)
#     if not products.exists():
#         return Response({"error": f"No products found in category: {category}"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


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
from Checkout.models import OrderHistory
class UpdateOrderStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, order_id):
        try:
            order = OrderHistory.objects.get(id=order_id)
        except OrderHistory.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            order_status = OrderStatus.objects.get(order=order)
        except OrderStatus.DoesNotExist:
            return Response({"error": "Status not found for this order."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderStatusSerializer(order_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        try:
            order = OrderHistory.objects.get(id=order_id)
        except OrderHistory.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in ['confirmed', 'shipped', 'delivered']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        order_status, created = OrderStatus.objects.get_or_create(order=order)
        order_status.status = new_status
        order_status.save()

        serializer = OrderStatusSerializer(order_status)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from .models import Inventory
from productmodule.models import Product
from .serializers import InventorySerializer

class UpdateInventoryView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get or create inventory record for the product
        inventory, created = Inventory.objects.get_or_create(product=product)

        new_inventory = request.data.get("inventory")
        if new_inventory is None:
            return Response({"error": "Inventory value is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inventory.inventory = int(new_inventory)  # Update the 'inventory' field
            inventory.save()
        except ValueError:
            return Response({"error": "Invalid inventory value."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllOrderStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_orders = OrderHistory.objects.all()

        # Ensure each order has a corresponding OrderStatus
        for order in all_orders:
            OrderStatus.objects.get_or_create(order=order, defaults={"status": "confirmed"})

        # Fetch all order statuses
        order_statuses = OrderStatus.objects.select_related('order').all()

        # Count totals
        delivered_count = order_statuses.filter(status="delivered").count()
        shipped_count = order_statuses.filter(status="shipped").count()
        confirmed_count = order_statuses.filter(status="confirmed").count()
        pending_count = shipped_count + confirmed_count

        serializer = OrderStatusSerializer(order_statuses, many=True)

        return Response({
            "order_statuses": serializer.data,
            "counts": {
                "delivered": delivered_count,
                "shipped": shipped_count,
                "pending": pending_count
            }
        }, status=status.HTTP_200_OK)
    

class GetAllInventoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Ensure every product has an inventory record
        all_products = Product.objects.all()

        for product in all_products:
            Inventory.objects.get_or_create(product=product, defaults={"quantity": 0})

        # Fetch all inventories (now guaranteed to include every product)
        inventories = Inventory.objects.select_related('product').all()
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)