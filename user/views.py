#This file contains the views for user authentication and profile management.
# It includes signup, login, and user profile retrieval functionalities.
# Implemented JWT authentication for secure access to user data.

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer
from uuid import UUID


# Generate JWT tokens
# This function generates JWT tokens for the user after successful authentication.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Signup API
# This API is used to register a new user. It accepts phone number, first name, last name, and password.
# The password is hashed before saving to the database.
@api_view(["POST"])
@permission_classes([AllowAny])  #  No authentication required
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        return Response(
            {"message": "User registered successfully", "tokens": tokens},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API
# This API is used to authenticate users and generate JWT tokens.
# It checks the provided phone number and password against the database.
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    phone = request.data.get("phone")
    password = request.data.get("password")

    try:
        user = User.objects.get(phone=phone)
    except (User.DoesNotExist, ValueError):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Ensure UUID is properly handled if accessed directly
        UUID(str(user.id))
    except ValueError:
        return Response({"error": "Invalid user ID format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    tokens = get_tokens_for_user(user)

    return Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)


# Get user profile (Protected)
# This is used to fetch the user profile information after login.
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Requires JWT authentication
def user_profile(request):
    user = request.user
    return Response(
        {"firstName": user.firstName, "lastName": user.lastName, "phone": user.phone},
        status=status.HTTP_200_OK,
    )
