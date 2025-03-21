from django import forms 
from django.contrib.auth.models import User
from .models import CustomUser, Play, Review, Category

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=25, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=25, required=True, help_text='Required. Enter your surname.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter a secure password.')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profilePicture', 'bio']