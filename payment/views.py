from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser

from .serializers import AdsSubscriberSerializer
from .services import PayboxRedirectService
from .models import AdsSubscriber


class AdsSubscriberListView(generics.ListAPIView):
    queryset = AdsSubscriber.objects.all()
    serializer_class = AdsSubscriberSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["advertisement", "is_paid"]
    search_fields = ["description"]


class AdsSubscriberAPIView(generics.CreateAPIView):
    serializer_class = AdsSubscriberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ads_subsriber = serializer.save()
        headers = self.get_success_headers(serializer.data)
        paybox_redirect = PayboxRedirectService.generate_paybox_url(ads_subsriber)

        return Response(
            {"redirect_url": paybox_redirect.get('url')}, status=status.HTTP_201_CREATED, headers=headers
        )

import requests

class SuccessPaymentAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        url = 'https://api.paybox.money/get_status2.php'
        response = request.post(url)
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
