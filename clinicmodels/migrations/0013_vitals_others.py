# Generated by Django 4.2 on 2023-12-05 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0012_vitals_left_eye_pinhole_vitals_right_eye_pinhole'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitals',
            name='others',
            field=models.TextField(blank=True, null=True),
        ),
    ]