# Generated by Django 3.0.7 on 2020-07-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='avail',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
