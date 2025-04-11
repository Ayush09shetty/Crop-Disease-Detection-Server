import uuid
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, CartItem
from productmodule.models import Product
from .serializers import CartItemSerializer

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        product_id = data.get("productID")
        quantity = data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert hex string to UUID format
            product_uuid = str(uuid.UUID(product_id))
            product = Product.objects.get(id=product_uuid)
        except (ValueError, Product.DoesNotExist):
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product.id)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        return Response({"message": "Product added to cart successfully!"}, status=status.HTTP_200_OK)

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        product_id = data.get("productID")
        quantity = data.get("quantity")

        if not product_id or quantity is None:
            return Response({"error": "Product ID and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        if int(quantity) == 0:
            cart_item.delete()
            return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)

        cart_item.quantity = int(quantity)
        cart_item.save()
        return Response({"message": "Cart item updated successfully!"}, status=status.HTTP_200_OK)


class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()
        # serializer = CartItemSerializer(cart_items, many=True)
        serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
        return Response(serializer.data)


class DeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        data = request.data
        product_id = data.get("productID")

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        cart_item.delete()
        return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)
