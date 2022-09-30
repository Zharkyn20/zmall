from rest_framework import serializers

from .models import AdsSubscriber


class AdsSubscriberSerializer(serializers.ModelSerializer):
    pg_amount = serializers.IntegerField(read_only=True)
    is_paid = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        ads_subscriber = super(AdsSubscriberSerializer, self).create(validated_data)
        delta_date = ads_subscriber.end_date - ads_subscriber.start_date

        ads_subscriber.pg_amount = delta_date.days * ads_subscriber.subscription.price
        ads_subscriber.save()

        return ads_subscriber

    class Meta:
        model = AdsSubscriber
        fields = ("advertisement", "subscription", "start_date", "end_date", "created_at", 'pg_amount', 'is_paid')
