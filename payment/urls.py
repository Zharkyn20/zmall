from django.urls import path

from .views import OrderPaymentListView, OrderPaymentAPIView, SuccessPaymentAPIView

urlpatterns = [
    path("list/", OrderPaymentListView.as_view(), name='payment_list'),
    path("payment/", OrderPaymentAPIView.as_view(), name='payment_create'),
    path("success/<int:pk>/", SuccessPaymentAPIView.as_view(), name='success_payment'),
]