# Generated by Django 3.0.7 on 2020-08-05 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_remove_address_colony'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
