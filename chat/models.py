from django.conf import settings
from django.db import models

from cloudinary.models import CloudinaryField

from advertisement.models import Advertisement


class Chat(models.Model):
    chat_id = models.CharField(verbose_name='Чат id', unique=True, db_index=True, max_length=50)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, related_name='chats')

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField(default='', blank=True)
    file = CloudinaryField('Файл', null=True, blank=True)
    send_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}:{self.chat}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['send_date']
