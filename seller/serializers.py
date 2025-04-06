from rest_framework import serializers
from .models import Seller

class SellerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['firstName', 'lastName', 'businessName', 'phone', 'email', 'gst', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Seller.objects.create_seller(**validated_data)

class SellerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            seller = Seller.objects.get(email=email)
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not seller.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        return seller
