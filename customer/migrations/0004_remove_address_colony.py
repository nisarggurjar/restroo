# Generated by Django 3.0.7 on 2020-08-05 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='colony',
        ),
    ]
