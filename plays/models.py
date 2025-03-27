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
    profile_pic = models.ImageField(upload_to='profile_images/', blank=True, null=True)

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
    LOCATION_CHOICES = [
        ("King's Theatre", "King's Theatre"),
        ("Theatre Royal", "Theatre Royal"),
        ("Pavilion Theatre", "Pavilion Theatre"),
        ("Glasgow Royal Concert Hall", "Glasgow Royal Concert Hall"),
        ("SEC Armadillo", "SEC Armadillo"),
        ("Tron Theatre", "Tron Theatre"),
        ("Citizens Theatre", "Citizens Theatre"),
    ]

    SPOTIFY_CHOICES = [
        ("lion_king", "The Lion King"),
        ("annie", "Annie, The Musical"),
        ("phantom_of_the_opera", "The Phantom of the Opera"),
        ("sound_of_music", "The Sound of Music"),
        ("book_of_mormon", "The Book of Mormon"),
        ("hamilton", "Hamilton"),
        ("wicked", "Wicked Soundtrack"),
        ("les_miserables", "Les Misérables"),
        ("mamma_mia", "Mamma Mia!"),
        ("dear_evan_hansen", "Dear Evan Hansen"),
        ]

    
    
    playID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    WriterFirstName = models.CharField(max_length=25)
    WriterSecondName = models.CharField(max_length=25)
    genre = models.CharField(max_length=25)
    releaseDate = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000)
    playImage = models.ImageField(upload_to='images/')
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default="King's Theatre")
    date_play= models.DateField(null=True, blank=True)
    spotifyCode = models.CharField(max_length=50, choices=SPOTIFY_CHOICES, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:   
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    
    LOCATION_CHOICES = [
        ("King's Theatre", "King's Theatre"),
        ("Theatre Royal", "Theatre Royal"),
        ("Pavilion Theatre", "Pavilion Theatre"),
        ("Glasgow Royal Concert Hall", "Glasgow Royal Concert Hall"),
        ("SEC Armadillo", "SEC Armadillo"),
        ("Tron Theatre", "Tron Theatre"),
        ("Citizens Theatre", "Citizens Theatre"),
    ]
    
    reviewID = models.AutoField(primary_key=True)
    playId = models.ForeignKey(Play, on_delete=models.CASCADE)  
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    SoundTrackRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    CastRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    SetRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    AverageRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000)
    playPicture = models.ImageField(upload_to='images/')
    
    def save(self, *args, **kwargs):
        total_ratings = sum(filter(None, [self.SoundTrackRating, self.CastRating, self.SetRating]))
        count = sum(1 for x in [self.SoundTrackRating, self.CastRating, self.SetRating] if x > 0)
        self.AverageRating = total_ratings / count if count else 0  # Avoid division by zero
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.username.username}"
    
    class Meta:
        unique_together = ('playId', 'username')


class Feedback(models.Model):
    feedbackID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_feedback')
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return f"Feedback by {self.username.username}"

