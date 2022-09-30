from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import AdsSubscriber, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'get_icon')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('get_icon',)

    def get_icon(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.icon.url} width="130" height="180">') if obj.icon else '-'

    get_icon.short_description = 'Иконка'


@admin.register(AdsSubscriber)
class AdsSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'subscription', 'pg_amount', 'start_date', 'end_date', 'created_at')
    list_display_links = ('id', 'advertisement', 'subscription')
    search_fields = ('advertisement', 'subscription')
    list_filter = ('advertisement', 'subscription', 'start_date', 'end_date', 'created_at')
