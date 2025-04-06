from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserAddress
from .serializers import UserAddressSerializer

class AddAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Create new address
        address = UserAddress.objects.create(
            user=user,
            line_one=data.get("line1"),
            line_two=data.get("line2"),
            street=data.get("street"),
            landmark=data.get("landmark"),
            city=data.get("city"),
            state=data.get("state"),
            zip_code=data.get("pincode"),
        )

        return Response({"message": "Address added successfully!", "id": address.id}, status=status.HTTP_201_CREATED)


class FetchAllAddressesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        addresses = UserAddress.objects.filter(user=user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        address_id = data.get("address_id")

        if not address_id:
            return Response({"error": "Address ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        address = get_object_or_404(UserAddress, id=address_id, user=user)

        # Update fields if provided
        address.line_one = data.get("line1", address.line_one)
        address.line_two = data.get("line2", address.line_two)
        address.street = data.get("street", address.street)
        address.landmark = data.get("landmark", address.landmark)
        address.city = data.get("city", address.city)
        address.state = data.get("state", address.state)
        address.zip_code = data.get("pincode", address.zip_code)

        address.save()

        return Response({"message": "Address updated successfully!"}, status=status.HTTP_200_OK)

class DeleteAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        data = request.data
        address_id = data.get("address_id")

        if not address_id:
            return Response({"error": "Address ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        address = get_object_or_404(UserAddress, id=address_id, user=user)

        address.delete()

        return Response({"message": "Address deleted successfully!"}, status=status.HTTP_200_OK)
class UpdateUserNameView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        fname = data.get("fname")
        lname = data.get("lname")

        if fname:
            user.first_name = fname
        if lname:
            user.last_name = lname

        user.save()

        return Response({"message": "User name updated successfully!"}, status=status.HTTP_200_OK)


class UpdateUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        old_password = data.get("oldPassword")
        new_password = data.get("newPassword")

        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)


        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)


class UpdateUserPhoneView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        phone = data.get("phone")

        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        user.profile.phone = phone  # Assuming there is a profile model linked to the user
        user.profile.save()

        return Response({"message": "Phone number updated successfully!"}, status=status.HTTP_200_OK)