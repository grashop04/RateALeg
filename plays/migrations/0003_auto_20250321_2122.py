# Generated by Django 2.2.28 on 2025-03-21 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plays', '0002_auto_20250321_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='play',
            name='date_play',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='play',
            name='location',
            field=models.CharField(default="King's Theatre", max_length=100),
        ),
    ]
