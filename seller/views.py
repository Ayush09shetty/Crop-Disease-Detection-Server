#This file contains the views for seller authentication token, login, profile details and signup functions
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
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
# This function is used for seller signup page
# This take feilds like seller details, gst number, phone number,email and genrate a jwt token for the seller
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
# This is a login functionality of the seller
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
# This function is used to fetch the seller details
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


# This function is used to fetch the seller id with the given seller token as the input
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # Important to prevent default JWT auth from interfering
def get_seller_id_from_token(request):
    token = request.data.get("token")

    if not token:
        return Response({"error": "Access token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Decode the token using SimpleJWT's AccessToken class
        access_token = AccessToken(token)
        user_id = access_token.get('user_id')

        if not user_id:
            return Response({"error": "Invalid token, user_id not found"}, status=status.HTTP_400_BAD_REQUEST)

        seller = Seller.objects.get(id=user_id)

        return Response({"seller_id": str(seller.id)}, status=status.HTTP_200_OK)

    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)