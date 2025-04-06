from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ConsultantUser
from .serializers import RegisterSerializer, ConsultantUserSerializer, LoginSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Generate JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# Consultant Registration
@permission_classes([AllowAny])
class ConsultantRegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Consultant registered successfully!", "tokens": get_tokens_for_user(user)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultantLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                user = ConsultantUser.objects.get(email=email)  # Fetch user by email
                if not user.check_password(password):  # Verify password manually
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
                
                return Response(
                    {"message": "Login successful", "tokens": get_tokens_for_user(user)},
                    status=status.HTTP_200_OK,
                )
            except ConsultantUser.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Consultant Profile

class ConsultantProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ConsultantUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
