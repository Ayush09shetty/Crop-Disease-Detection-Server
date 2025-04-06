import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderHistory
from .serializers import OrderHistorySerializer
from productmodule.models import Product
from Cart.models import Cart, CartItem


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({"error": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST)

            # Extract and validate data
            address = request.data.get("address")
            transaction_id = request.data.get("transaction_id")
            payment_id = request.data.get("payment_id")
            payment_method = request.data.get("payment_method", "").lower()
            payment_status = request.data.get("payment_status", "").lower()

            if not all([address, transaction_id, payment_id, payment_method, payment_status]):
                return Response({"error": "Missing fields in request."}, status=status.HTTP_400_BAD_REQUEST)

            if payment_method not in ['online', 'offline']:
                return Response({"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST)

            if payment_status not in ['pending', 'success', 'failed']:
                return Response({"error": "Invalid payment status."}, status=status.HTTP_400_BAD_REQUEST)

            order_history_id = str(uuid.uuid4())

            # Calculate total amount from cart
            total_amount = 0
            for cart_item in cart_items:
                total_amount += cart_item.product.selling_price * cart_item.quantity

            # Create OrderHistory
            order_history = OrderHistory.objects.create(
                id=order_history_id,
                user=user,
                user_address=address,
                total_amount=total_amount,
                transaction_id=transaction_id,
                payment_id=payment_id,
                payment_method=payment_method,
                payment_status=payment_status,
                order_status='confirmed'
            )

            # Create individual orders
            for cart_item in cart_items:
                product = cart_item.product
                rate = product.selling_price
                quantity = cart_item.quantity
                total_price = rate * quantity

                Order.objects.create(
                    id=str(uuid.uuid4()),
                    order_history=order_history,
                    product=product,
                    quantity=quantity,
                    rate=rate,
                    total_price=total_price
                )

            # Clear the cart
            cart_items.delete()
            cart.delete()

            serializer = OrderHistorySerializer(order_history)
            return Response({
                "message": "Order placed successfully.",
                "order": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchOrderSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = OrderHistory.objects.filter(user=user).order_by('-order_date')
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
