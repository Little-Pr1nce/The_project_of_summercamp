# Generated by Django 2.0.7 on 2018-07-25 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_bill_dish_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='dish_table',
            field=models.IntegerField(default=0),
        ),
    ]
