# Generated by Django 5.1.7 on 2025-03-28 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plays', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='spotifyCode',
            field=models.CharField(blank=True, choices=[('lion_king', 'The Lion King'), ('annie', 'Annie, The Musical'), ('phantom_of_the_opera', 'The Phantom of the Opera'), ('sound_of_music', 'The Sound of Music'), ('book_of_mormon', 'The Book of Mormon'), ('hamilton', 'Hamilton'), ('wicked', 'Wicked'), ('les_miserables', 'Les Misérables'), ('mamma_mia', 'Mamma Mia!'), ('dear_evan_hansen', 'Dear Evan Hansen')], max_length=50, null=True),
        ),
    ]
