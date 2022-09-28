from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField

from advertisement.models import Advertisement

from .manager import UserManager
from .utils import JWTAuth


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField('Name', max_length=100)
    last_name = models.CharField('Surname', max_length=100)
    phone_number = PhoneNumberField('Номер телефона')

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'phone_number'
    )

    def get_token(self):
        jwt_auth = JWTAuth()
        token = jwt_auth.get_by_user(self)
        jwt_auth.close()

        return {
            'access': token
        }

    def has_module_perms(self, app_label):
        return self.is_staff or self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
