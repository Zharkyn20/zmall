# Generated by Django 4.1 on 2022-09-17 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0009_favorite_delete_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adssubscriber',
            name='advertisement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriber', to='advertisement.advertisement', verbose_name='Объявление'),
        ),
    ]
