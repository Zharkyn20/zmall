from datetime import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from advertisement.filters import AdvertisementCustomFilterBackend
from advertisement.swagger_scheme import (
    AdvertisementQuerySerializer,
    child_category_id_query,
    limit_query
)

from advertisement.permissions import IsOwnerOrSuperUser

from advertisement.serializers import (
    AdvertisementSerializer,
    AdvertisementRetrieveSerializer,
    ComplainingForAdsSerializer
)

from advertisement.models import (
    ChildCategory,
    Advertisement,
    ComplainingForAds,
    AdsImage
)

from payment.models import AdsSubscriber


class AdvertisementListView(generics.ListAPIView):
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementCustomFilterBackend)
    filterset_fields = ('child_category_id', 'disable_date')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    @swagger_auto_schema(method='get', query_serializer=AdvertisementQuerySerializer)
    @action(['get'], detail=False)
    def get(self, request, *args, **kwargs):
        return super(AdvertisementListView, self).get(request)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(type=settings.ACTIVE)

        if self.request.user.is_superuser:
            queryset = Advertisement.objects.all()

        return queryset


class AdvertisementCreateView(generics.CreateAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        data = request.data

        context_data = {
            'images': images,
            'owner': request.user
        }

        serializer = self.get_serializer(data=data, context=context_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdvertisementRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    def update(self, request, *args, **kwargs):
        del_images = request.data.get('del_images')
        AdsImage.objects.in_bulk(del_images).delete()

        ads_img_count = AdsImage.objects.filter(advertisement=self.get_object()).count()
        images = request.FILES.getlist('images')

        if ads_img_count + len(images) > 8:
            return Response({'images': 'images more then 8!'}, status=status.HTTP_400_BAD_REQUEST)

        for key, file in request.FILES.items():
            if '_' not in key:
                continue

            img_id = int(key.split('_'))
            img = AdsImage.objects.get(pk=img_id)
            img.image = file
            img.save()

        super(AdvertisementRUDView, self).update(request, *args, **kwargs)

        return Response({'message': 'success'}, status=status.HTTP_202_ACCEPTED)


class UserAdvertisementListView(generics.ListAPIView):
    """You can filter by Активный - На проверке - Неактивный. And search by name!"""
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('type',)
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(owner=self.request.user)
        return queryset


class SimularAdsView(views.APIView):
    @swagger_auto_schema(method='get', manual_parameters=[limit_query, child_category_id_query])
    @action(methods=['GET'], detail=False)
    def get(self, request, child_category_id, *args, **kwargs):
        """Get child category id"""
        limit = self.request.query_params.get('limit')

        if limit:
            limit = int(limit)
        else:
            limit = 5

        child_category = get_object_or_404(ChildCategory, pk=child_category_id)

        advertisement = (
            Advertisement.objects
            .select_related('child_category')
            .filter(child_category=child_category)
            [:limit]
        )

        serializer = AdvertisementRetrieveSerializer(advertisement, many=True, context={'request': request})
        return Response({'count': advertisement.count(), 'results': serializer.data}, status=status.HTTP_200_OK)


class ComplainingForAdsView(generics.CreateAPIView):
    queryset = ComplainingForAds.objects.all()
    serializer_class = ComplainingForAdsSerializer
    permission_classes = [IsAuthenticated]


class AdsSubscriberAPIView(generics.ListAPIView):
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        date = datetime.now(tz=timezone.get_current_timezone())
        instance = AdsSubscriber.objects.filter(end_date__gte=date)
        return Advertisement.objects.filter(subscriber__in=instance)
