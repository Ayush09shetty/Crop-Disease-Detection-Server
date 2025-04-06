from rest_framework import serializers
from .models import ConsultantUser

class ConsultantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantUser
        fields = ["id", "first_name", "last_name", "phone", "email", "expertise", "experience", "starting_charges", "profile"]
        extra_kwargs = {"profile": {"required": False}}

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantUser
        fields = ["first_name", "last_name", "phone", "email", "expertise", "experience", "starting_charges", "profile", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_image = validated_data.pop("profile", None)
        user = ConsultantUser.objects.create_user(**validated_data)

        # Save profile image if provided
        if profile_image:
            user.profile = profile_image
            user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
