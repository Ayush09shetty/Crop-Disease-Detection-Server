from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import Seller
from django.shortcuts import get_object_or_404
from .serializers import SellerSignupSerializer, SellerLoginSerializer

# Generate JWT tokens
def get_tokens_for_seller(seller):
    refresh = RefreshToken.for_user(seller)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Seller Signup API
@api_view(["POST"])
@permission_classes([AllowAny])  
def seller_signup(request):
    serializer = SellerSignupSerializer(data=request.data)
    if serializer.is_valid():
        seller = serializer.save()
        tokens = get_tokens_for_seller(seller)

        return Response(
            {"message": "Seller registered successfully", "tokens": tokens},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Seller Login API
@api_view(["POST"])
@permission_classes([AllowAny]) 
def seller_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        seller = Seller.objects.get(email=email)
    except Seller.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not seller.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    tokens = get_tokens_for_seller(seller)

    return Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)

# Get Seller Profile (Protected)
@api_view(['GET'])
@permission_classes([AllowAny])
def seller_profile(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)

    data = {
        "id": str(seller.id),
        "firstName": seller.firstName,
        "lastName": seller.lastName,
        "businessName": seller.businessName,
        "email": seller.email,
        "phone": seller.phone,
        "gst": seller.gst
    }
    return Response(data)
