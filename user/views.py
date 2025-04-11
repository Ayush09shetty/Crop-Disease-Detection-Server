from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer

# Generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Signup API
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
from uuid import UUID

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
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Requires JWT authentication
def user_profile(request):
    user = request.user
    return Response(
        {"firstName": user.firstName, "lastName": user.lastName, "phone": user.phone},
        status=status.HTTP_200_OK,
    )
