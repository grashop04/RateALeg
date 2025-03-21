# Generated by Django 2.2.28 on 2025-03-21 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plays', '0003_auto_20250321_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='location',
            field=models.CharField(choices=[("King's Theatre", "King's Theatre"), ('Theatre Royal', 'Theatre Royal'), ('Pavilion Theatre', 'Pavilion Theatre'), ('Glasgow Royal Concert Hall', 'Glasgow Royal Concert Hall'), ('SEC Armadillo', 'SEC Armadillo'), ('Tron Theatre', 'Tron Theatre'), ('Citizens Theatre', 'Citizens Theatre')], default="King's Theatre", max_length=100),
        ),
    ]
