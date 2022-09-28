from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from .serializers import OrderPaymentSerializer
from .services import PayboxRedirectService
from .models import OrderPayment


class OrderPaymentListView(generics.ListAPIView):
    serializer_class = OrderPaymentSerializer
    queryset = OrderPayment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["user_name", "advertisement", "is_paid"]
    search_fields = ["user_name", "description"]
    pagination_class = LimitOffsetPagination


class OrderPaymentAPIView(generics.CreateAPIView):
    serializer_class = OrderPaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donate = serializer.save()
        headers = self.get_success_headers(serializer.data)
        paybox_redirect = PayboxRedirectService.generate_paybox_url(donate)
        return Response(
            {"redirect_url": paybox_redirect}, status=status.HTTP_201_CREATED, headers=headers
        )


class SuccessPaymentAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        order_id = data.get('pg_order_id')
        OrderPayment.objects.get(pk=order_id).update(is_paid=True)
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
