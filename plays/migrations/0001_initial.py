# Generated by Django 2.2.28 on 2025-03-26 13:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('firstName', models.CharField(max_length=25)),
                ('secondName', models.CharField(max_length=25)),
                ('bio', models.CharField(blank=True, max_length=250)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('playID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('WriterFirstName', models.CharField(max_length=25)),
                ('WriterSecondName', models.CharField(max_length=25)),
                ('genre', models.CharField(max_length=25)),
                ('releaseDate', models.DateField()),
                ('description', models.TextField(max_length=1000)),
                ('playImage', models.ImageField(upload_to='images/')),
                ('location', models.CharField(choices=[("King's Theatre", "King's Theatre"), ('Theatre Royal', 'Theatre Royal'), ('Pavilion Theatre', 'Pavilion Theatre'), ('Glasgow Royal Concert Hall', 'Glasgow Royal Concert Hall'), ('SEC Armadillo', 'SEC Armadillo'), ('Tron Theatre', 'Tron Theatre'), ('Citizens Theatre', 'Citizens Theatre')], default="King's Theatre", max_length=100)),
                ('date_play', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('spotify_code', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedbackID', models.UUIDField(primary_key=True, serialize=False)),
                ('comment', models.TextField(max_length=1000)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_feedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewID', models.AutoField(primary_key=True, serialize=False)),
                ('SoundTrackRating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('CastRating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('SetRating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('AverageRating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(max_length=1000)),
                ('playPicture', models.ImageField(upload_to='images/')),
                ('playId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plays.Play')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('playId', 'username')},
            },
        ),
    ]
