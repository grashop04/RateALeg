from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

## May need to chnge this database a bit, unsure if password and such is actually required ?!
class CustomUser(AbstractUser):
    firstName = models.CharField(max_length=25)
    secondName = models.CharField(max_length=25)
    bio = models.CharField(max_length=250, blank=True)
    profilePicture = models.ImageField(upload_to='profile_images/', default='default-profile-pic.jpg')

    def __str__(self):
        return self.username

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Play(models.Model):
    playID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    WriterFirstName = models.CharField(max_length=25)
    WriterSecondName = models.CharField(max_length=25)
    genre = models.CharField(max_length=25)
    releaseDate = models.DateField()
    description = models.TextField(max_length=1000)
    playImage = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:   
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    playId = models.ForeignKey(Play, on_delete=models.CASCADE)  
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    SoundTrackRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    CastRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    SetRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    AverageRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000)
    playPicture = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Review by {self.username.username}"


class Feedback(models.Model):
    feedbackID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_feedback')
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return f"Feedback by {self.username.username}"

