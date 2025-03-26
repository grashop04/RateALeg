from django.test import TestCase, Client
from django.urls import reverse
from plays.models import Play, CustomUser, Review
from django.utils import timezone
from datetime import date

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testingUser',
            password='password123',
            firstname='testfirstname',
            secondName=' testsecondName'
        )

        self.play = Play.objects.create(
            title="tetstitle",
            WriterFirstName="Testfirstname",
            WriterSecondName="WritersecondName",
            genre="play test",
            releaseDate=date.today(),
            description="This is a test play.",
            location="King's Theatre",
            slug="test-play",
        )

        self.review = Review.objects.create(
            playId=self.play,
            username=self.user,
            SoundTrackRating = 4,
            CastRating=5,
            SetRating=3,
            AverageRating=4,
            comment="Testing I Loved it!",
        )
   
    
