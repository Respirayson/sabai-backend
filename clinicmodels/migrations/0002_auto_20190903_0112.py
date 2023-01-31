# Generated by Django 2.2.4 on 2019-09-03 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='reserve_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Order Completed', max_length=255),
            preserve_default=False,
        ),
    ]
