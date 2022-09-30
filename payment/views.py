import json

from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny

from advertisement.utils import Redis
from .serializers import AdsSubscriberSerializer, SubscriptionSerializer
from .services import PayboxRedirectService
from .models import AdsSubscriber, Subscription
from .tasks import check_payment


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
        redirect_url = PayboxRedirectService.generate_paybox_url(ads_subsriber)

        # redis = Redis()
        # conn = redis.conn
        # conn.set(f'payment-{ads_subsriber.pk}', json.dumps(paybox_response))

        # redis.close()

        return Response(
            {"redirect_url": redirect_url}, status=status.HTTP_201_CREATED, headers=headers
        )


class SuccessPaymentAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        order_id = data.get('pg_order_id')
        AdsSubscriber.objects.filter(pk=order_id).update(is_paid=True)

        return Response({"message": "Success"}, status=status.HTTP_200_OK)


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]
