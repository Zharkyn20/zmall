# Generated by Django 4.1 on 2022-08-30 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0010_remove_advertisement_head_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='type',
            field=models.CharField(choices=[('A', 'Активный'), ('C', 'На проверке'), ('D', 'Неактивен')], default='C', max_length=1, verbose_name='Статус объявления'),
        ),
    ]