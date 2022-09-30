from django.urls import path

from .views import (
    RegisterUserView,
    LoginAPIView,
    UserActivationView,
    UserRetrieveUpdateAPIView,
    SendMassAPIView,
    ForgotPasswordAPIView,
)

urlpatterns = [
    path('', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('activation/', UserActivationView.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('send-mass/', SendMassAPIView.as_view(), name='send_mass'),
]
