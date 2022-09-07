# Generated by Django 4.1 on 2022-09-07 06:01

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(choices=[('Жалоба', 'Жалоба'), ('Предложение', 'Предложение')], default='Жалоба', max_length=20, verbose_name='Тема сообщения')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('send_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('check_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата проверки')),
                ('checked', models.BooleanField(default=False, verbose_name='Проверена')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратная связь',
            },
        ),
        migrations.CreateModel(
            name='HelpCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория помощи',
                'verbose_name_plural': 'Категории помощи',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название сайта')),
                ('logo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Логотип')),
                ('privacy_policy_text', models.TextField(max_length=5000, verbose_name='Политика конфиденциальности текст')),
                ('copyright', models.CharField(max_length=20, verbose_name='Авторские права')),
            ],
            options={
                'verbose_name': 'Информация о сайте',
                'verbose_name_plural': 'Информация о сайтах',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Изображение')),
                ('type', models.CharField(choices=[('Social Networks', 'Social Networks'), ('App', 'App')], default='Social Networks', max_length=20, verbose_name='Тип')),
                ('link', models.CharField(max_length=100, verbose_name='Ссылка')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='siteapp.site', verbose_name='Сайт')),
            ],
            options={
                'verbose_name': 'Cоц-медия',
                'verbose_name_plural': 'Соц-медии',
            },
        ),
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Загаловок')),
                ('text', models.TextField(max_length=5000, verbose_name='Текст')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='help', to='siteapp.helpcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Помощь',
                'verbose_name_plural': 'Помощь',
            },
        ),
    ]
