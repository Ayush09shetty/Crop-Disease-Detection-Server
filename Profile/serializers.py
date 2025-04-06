from rest_framework import serializers
from .models import UserAddress

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ["id", "line_one", "line_two", "street", "landmark", "city", "state", "country", "zip_code"]
