# Generated by Django 4.2 on 2023-12-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0011_alter_vitals_left_eye_degree_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitals',
            name='left_eye_pinhole',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vitals',
            name='right_eye_pinhole',
            field=models.TextField(blank=True, null=True),
        ),
    ]
