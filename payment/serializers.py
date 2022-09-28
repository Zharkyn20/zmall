from rest_framework import serializers

from .models import OrderPayment


class OrderPaymentSerializer(serializers.ModelSerializer):
    is_paid = serializers.BooleanField(read_only=True)
    class Meta:
        model = OrderPayment
        fields = ("advertisement", "user_name", "description", "created_at", "amount", 'is_paid')
