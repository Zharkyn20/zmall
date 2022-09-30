from cloudinary.models import CloudinaryField
from django.db import models

from advertisement.models import Advertisement


class Subscription(models.Model):
    name = models.CharField('Название', max_length=100)
    price = models.PositiveIntegerField('Цена', default=0)
    icon = CloudinaryField('Иконка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']


class AdsSubscriber(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, verbose_name='Объявление', blank=True,
                                      null=True, related_name='subscriber')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, verbose_name='Подписка', blank=True,
                                     null=True)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    created_at = models.DateTimeField('Дата создания', auto_now=True)
    pg_amount = models.PositiveIntegerField(null=True, blank=True)
    is_paid = models.BooleanField("Оплачено", default=False)

    def __str__(self):
        return self.advertisement.name

    class Meta:
        verbose_name = 'Подписка объявления'
        verbose_name_plural = 'Подписки объявлений'
        ordering = ['id']
