# Generated by Django 4.2 on 2023-05-03 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicmodels', '0001_squashed_0007_remove_visitconsult_consult_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vitals',
            name='cataracts_scale',
        ),
        migrations.AddField(
            model_name='vitals',
            name='cataracts',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vitals',
            name='eye_pressure',
            field=models.TextField(blank=True, null=True),
        ),
    ]