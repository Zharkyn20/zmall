# Generated by Django 4.1 on 2022-09-29 06:48

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_message_send_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]