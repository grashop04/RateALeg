from django import forms 
from django.contrib.auth.models import User
from .models import CustomUser, Play, Review, Category

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['SoundTrackRating', 'CastRating', 'SetRating', 'comment']
        widgets = {
            'soundtrack_rating': forms.HiddenInput(),
            'cast_rating': forms.HiddenInput(),
            'set_rating': forms.HiddenInput(),
            'comment':forms.Textarea(attrs={'rows':4}),
        }

