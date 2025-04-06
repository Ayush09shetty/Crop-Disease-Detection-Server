# urls.py

from django.urls import path
from .views import AddSearchHistoryView, GetSearchHistoryView

urlpatterns = [
    path('add/', AddSearchHistoryView.as_view(), name='add-search'),
    path('history/', GetSearchHistoryView.as_view(), name='get-search-history'),
]
