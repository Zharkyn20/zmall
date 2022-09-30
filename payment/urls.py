from django.urls import path

from .views import AdsSubscriberListView, AdsSubscriberAPIView, SuccessPaymentAPIView

urlpatterns = [
    path("list/", AdsSubscriberListView.as_view(), name='payment_list'),
    path("payment/", AdsSubscriberAPIView.as_view(), name='payment_create'),
    path("success/", SuccessPaymentAPIView.as_view(), name='success_payment'),
]
