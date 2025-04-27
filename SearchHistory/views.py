# views.py
# This function is used to store the search history and view all the search history
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SearchHistory
from .serializers import SearchHistorySerializer


# This function is used to add the search history
class AddSearchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        search_query = request.data.get("search_query")

        if not search_query:
            return Response({"error": "search_query is required."}, status=status.HTTP_400_BAD_REQUEST)

        search = SearchHistory.objects.create(user=request.user, search_query=search_query)
        serializer = SearchHistorySerializer(search)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# This function is used to fetch all the search history
class GetSearchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        searches = SearchHistory.objects.filter(user=request.user).order_by("-searched_at")
        serializer = SearchHistorySerializer(searches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
