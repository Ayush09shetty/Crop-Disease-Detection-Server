from rest_framework_simplejwt.authentication import JWTAuthentication
from seller.models import Seller
from rest_framework.exceptions import AuthenticationFailed

class SellerJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        try:
            return Seller.objects.get(id=user_id)
        except Seller.DoesNotExist:
            raise AuthenticationFailed("Seller not found", code="user_not_found")
