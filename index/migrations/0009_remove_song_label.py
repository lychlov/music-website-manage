# Generated by Django 2.2.5 on 2022-12-08 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20221208_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='label',
        ),
    ]
