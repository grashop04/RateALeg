from django import forms 
from django.contrib.auth.models import User
from .models import CustomUser, Play, Review, Category

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['SoundTrackRating', 'CastRating', 'SetRating', 'AverageRating', 'comment']

