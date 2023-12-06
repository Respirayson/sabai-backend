# Generated by Django 4.2 on 2023-12-06 00:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0015_alter_vitals_diabetes_mellitus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]