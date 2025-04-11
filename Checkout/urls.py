from django.urls import path
from .views import PlaceOrderView, FetchOrderSummaryView, razorpayorder

urlpatterns = [
    path("placeorder/", PlaceOrderView.as_view(), name="place_order"),
    path("fetch-order-summary/", FetchOrderSummaryView.as_view(), name="fetch_order_summary"),
    path("create_order/", razorpayorder, name="razorpayorder"),  # ✅ Correct view name, no .as_view()
]
