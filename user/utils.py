import datetime

import redis
import jwt

from django.conf import settings
from django.utils import timezone


class JWTAuth:
    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        self.key = settings.JWT_CONFIG.get('SIGNING_KEY')
        self.algorithm = settings.JWT_CONFIG.get('ALGORITHM')
        self.token_life = settings.JWT_CONFIG.get('TOKEN_LIFETIME')
        self.header_type = settings.JWT_CONFIG.get('AUTH_HEADER_TYPES')

    def generate_jwt_token(self, user):
        dt = datetime.datetime.now(tz=timezone.get_default_timezone()) + self.token_life

        token = jwt.encode({
            'id': user.pk,
            'exp': int(dt.strftime('%s'))
        }, self.key, algorithm=self.algorithm)

        return token

    def get_by_token(self, token_key):
        header_type, token = token_key.split()

        if not self.check_header_type(header_type):
            return

        if self.check_blocked_token(token_key):
            return

        data = jwt.decode(token, self.key, algorithms=[self.algorithm])

        return data.get('id')

    def get_by_user(self, user):
        token = self.generate_jwt_token(user)
        return token

    def block_token(self, token):
        self.conn.set(token, 1)

    def check_blocked_token(self, token):
        return True if self.conn.get(token) else False

    def check_header_type(self, header_type):
        return True if self.header_type == header_type else False

    def close(self):
        self.conn.close()


def get_token_in_headers(request):
    token = request.headers.get('Authorization')
    return token
