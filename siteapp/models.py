from django.db import models


class Site(models.Model):
    name = models.CharField('Название сайта', max_length=100)
    logo = models.ImageField('Логотип ', upload_to='site_image/')
    privacy_policy_title = models.CharField('Политика конфиденциальности название', max_length=100)
    privacy_policy_text = models.TextField('Политика конфиденциальности текст', max_length=5000)
    copyright = models.CharField('Авторские права', max_length=20)


class SocialMedia(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', upload_to='site_image/link_image/')
    type = models.CharField('Тип', max_length=100)
    link = models.CharField('Ссылка', max_length=100)
    site = models.ForeignKey(Site, verbose_name='Сайт', on_delete=models.DO_NOTHING)


class FeedBack(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField()
    subject = models.CharField('Тема сообщения', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    send_date = models.DateTimeField('Дата отправки', auto_now_add=True)
    check_date = models.DateTimeField('Дата проверки', null=True, blank=True)
    checked = models.BooleanField('Проверена', default=0)


class Help(models.Model):
    title = models.CharField('Загаловок', max_length=100)
    text = models.TextField('Текст', max_length=5000)
