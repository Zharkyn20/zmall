from django.urls import path

from .views import OrderPaymentListView, OrderPaymentAPIView, SuccessPaymentAPIView

urlpatterns = [
    path("list/", OrderPaymentListView.as_view()),
    path("payment/", OrderPaymentAPIView.as_view()),
    path("success/<int:pk>/", SuccessPaymentAPIView.as_view()),
]