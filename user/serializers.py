from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'firstName', 'lastName', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid phone number or password")

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return {
            'user_id': str(user.id),  # UUID returned as string
            'firstName': user.firstName,
            'lastName': user.lastName,
            'phone': user.phone,
            'tokens': tokens
        }
