# Generated by Django 2.0.7 on 2018-07-24 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20180723_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='dish_price',
            field=models.IntegerField(default=0),
        ),
    ]
