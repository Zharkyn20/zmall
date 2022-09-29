import random

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from advertisement.utils import Redis

from .models import User
from .tasks import send_activation_mail
from .utils import get_token_in_headers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        # Вызвать исключение, если не предоставлена почта.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Вызвать исключение, если не предоставлен пароль.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=email, password=password)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django предоставляет флаг is_active для модели User. Его цель
        # сообщить, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            'email': user.email,
            'token': user.token
        }

# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email уже используется')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        activation_code = random.randint(1000, 9999)

        redis = Redis()
        key = f'activate_code_{activation_code}'
        redis.conn.set(key, user.pk)
        redis.conn.expire(key, 3600)
        redis.close()

        send_activation_mail.delay(user.email, activation_code)
        return user

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'password_confirm',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
        )


class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(required=False, allow_null=True)
    password_confirm = serializers.CharField(required=False, allow_null=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('password_confirm')

        if password:
            if not confirm_password:
                raise serializers.ValidationError({'password_confirm': 'Can\'t be empty, if password field exists!'})

            if password != confirm_password:
                raise serializers.ValidationError({'password_confirm': 'Passwords don\'t match!'})

            del data['password_confirm']
        else:
            if confirm_password:
                raise serializers.ValidationError({'password': 'Can\'t be empty, if password_confirm field exists!'})

        return data

    def update(self, user, data):
        validated_data = self.validate(data)

        password = validated_data.get('password')

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if email:
            user.email = email

        if phone_number:
            user.phone_number = phone_number

        if password:
            old_token = get_token_in_headers(self.context.get('request'))
            token = RefreshToken(old_token)
            token.blacklist()

            user.set_password(password)
            del validated_data['password']

        user.save()
        return user
