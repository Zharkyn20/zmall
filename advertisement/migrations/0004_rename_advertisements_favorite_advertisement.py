# Generated by Django 4.1 on 2022-09-20 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0003_alter_adsimage_options_alter_adssubscriber_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='advertisements',
            new_name='advertisement',
        ),
    ]
