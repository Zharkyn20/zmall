from django.utils import timezone
from django.http import HttpResponseForbidden

from rest_framework import status
from rest_framework.generics import get_object_or_404

from advertisement.models import Advertisement
from advertisement.views.advertisement_views import AdvertisementRUDView
from advertisement.utils import get_client_ip, Redis

from user.utils import JWTAuth, get_token_in_headers


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_auth = JWTAuth()
        token = get_token_in_headers(request)

        if token:
            jwt_auth.get_by_token(token)

        jwt_auth.close()

        response = self.get_response(request)

        return response


class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = get_client_ip(request)
        request.ip = user_ip
        response = self.get_response(request)

        return response


class RequestLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redis = Redis()
        client_ip = request.ip

        key = f'request-{client_ip}'

        conn = redis.conn
        request_count = conn.get(key)

        if not request_count:
            conn.set(key, 10)
            conn.expire(key, 10)
        else:
            query_count = int(request_count)

            if query_count == 0:
                return HttpResponseForbidden({'message': 'Request limit exceeded'},
                                             status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED)

        conn.decr(key)

        response = self.get_response(request)
        redis.close()

        return response


class ViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if view_func.cls == AdvertisementRUDView and request.method == 'GET':
                pk = view_kwargs.get('pk', None)
                instance = get_object_or_404(Advertisement, pk=pk)
                redis = Redis()
                ads_id = instance.pk
                date = timezone.now().date().strftime('%d.%m.%Y')
                client_ip = request.ip
                redis.add_views(ads_id, date, client_ip)
                redis.close()

        except AttributeError:
            pass

