# Generated by Django 5.1.7 on 2025-03-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plays', '0004_alter_customuser_first_name_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profilePicture',
            field=models.ImageField(default='default-profile-pic.jpg', upload_to='images/'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
