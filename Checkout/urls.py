from django.urls import path
from .views import PlaceOrderView, FetchOrderSummaryView, razorpayorder,FetchAllOrderHistoriesView,total_sales_by_seller,total_sales_profit_per_day,TopSellingProductsView

urlpatterns = [
    path("placeorder/", PlaceOrderView.as_view(), name="place_order"),
    path("fetch-order-summary/", FetchOrderSummaryView.as_view(), name="fetch_order_summary"),
    path("create_order/", razorpayorder, name="razorpayorder"), 
    path("fetch-all-order-histories/", FetchAllOrderHistoriesView.as_view(), name="fetch_all_order_histories"),
    path("total_sales_by_seller/", total_sales_by_seller, name="total_sales_by_seller"),
    path("total_sales_profit_per_day/", total_sales_profit_per_day, name="total_sales_profit_per_day"),
    path("TopSellingProductsView/", TopSellingProductsView.as_view(), name="TopSellingProductsView"),
]
