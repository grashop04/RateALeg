import json
from django.test import TestCase, SimpleTestCase
from plays.models import CustomUser, Feedback, Play, Category, Review

import os
import re
import inspect
import tempfile
import plays.models
from plays import forms
from populate_plays import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


#test the show page
class ShowsViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Comedy")
        self.play1 = Play.objects.create(
            title="Play 1", genre=self.category, releaseDate="2022-01-01"
        )
        self.play2 = Play.objects.create(
            title="Play 2", genre=self.category,  releaseDate="2023-01-01"
        )
        self.play3 = Play.objects.create(
            title="Play 3", genre=self.category,  releaseDate="2021-01-01"
        )

    #tests to see if the plays show up on the home page
    def test_shows_view(self):
        response = self.client.get(reverse('plays:shows'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Play 1")
        self.assertContains(response, "Play 2")
        self.assertContains(response, "Play 3")

   

    def test_shows_alphabetical(self):
        response = self.client.get(reverse('plays:shows') + '?sort=title')
        self.assertEqual(response.status_code, 200)
        plays_titles = [play.title for play in response.context['plays']]  
        self.assertEqual(plays_titles, ['Play 1', 'Play 2', 'Play 3'])





#about view
#tests simple cases - it loads, contains the correct content
class TestAboutPage(SimpleTestCase):
    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code,200)

    def test_about_page_correct_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'plays/about.html')
    
    def test_about_page_contains_correct_content(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'About Rate A Leg') 

##Testing maps view
##tests the API works
class TestMapsPage(SimpleTestCase):
    def test_maps_page_status_code(self):
        # Test that the maps page loads everything correctly
        response = self.client.get(reverse('plays:maps'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plays/maps.html')
        self.assertContains(response, "https://www.google.com/maps/embed/v1/search?key=")
        self.assertContains(response, 'http://kingstheatre')  # Verify the URL for King's Theatre
        self.assertContains(response, 'http://theatreroyalglasgow.net/')  # Verify the URL for Theatre Royal
        self.assertContains(response, 'https://trafalgartickets.com/pavilion-theatre-glasgow/en-GB')
        self.assertIn('googleapi', response.context)  # Make sure the API URL is in the context
        self.assertEqual(response.context['googleapi'], f"https://www.google.com/maps/embed/v1/search?key={settings.API_KEY}&q=theatres+Glasgow+City")



#login
class UserLoginTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='usertest', password='userpassword', email='usertest@example.com', 
                                             first_name='john', last_name='doe')
        
    #tests a valid user login
    def test_valid_login(self):
        response = self.client.post((reverse('login')), {'username': 'usertest', 'password':'userpassword'})
        self.assertRedirects(response, reverse('shows'))
        self.assertEqual(response.status_code, 302)

    #tests a mismatched password trying to login
    def test_invalid_password(self):
        response = self.client.post('/login/', {'username' : 'usertest', 'password':'wrongpassword'})
        self.assertContains(response, 'Invalid login details supplied.')
        self.assertEqual(response.status_code, 200)

    #tests a mismatched username trying to login
    def test_invalid_username(self):
        response = self.client.post('/login/', {'username' : 'wronguser', 'password':'userpassword'})
        self.assertContains(response, 'Invalid login details supplied.')
        self.assertEqual(response.status_code, 200)



 #signup tests   
class UserSignUpTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='usertest', password='userpassword', email='usertest@example.com', 
                                             first_name='john', last_name='doe')
        
    ##tests a valid signup
    def test_valid_signup(self):
        response = self.client.post(reverse('plays:signup'), {
            'username' : 'johnny',
            'email' : 'johndoe@example.com',
            'password' : 'doejohnoednhoj',
            'first_name': 'John',
            'last_name' : 'Doe'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='johnny').exists())
        self.assertRedirects(response, reverse('shows'))

    #tries to sign up with an invalid email address
    def test_invalid_signup_email(self):
        response = self.client.post(reverse('plays:signup'), {
            'username' : 'johnny',
            'email' : 'johndoeexample.com',
            'password' : 'doejohnoednhoj',
            'first_name': 'John',
            'last_name' : 'Doe'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    #tries to signup without inputting any data
    def test_invalid_signup_blank_fields(self):
        response = self.client.post(reverse('plays:signup'), {
            'username' : '',
            'email' : '',
            'password' : '',
            'first_name': '',
            'last_name' : ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
        


#feedback form
class FeedbackTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='usertest', password='userpassword', email='usertest@example.com', 
                                             first_name='john', last_name='doe')
        
        self.url = reverse('plays:feedback')
        
    #a logged in user successfully submits feedback
    def test_submit_valid_feedback(self):
        self.client.login(username='usertest', password='userpassword')
        feedback_data = {'feedback': 'This is a valid feedback'}
        response = self.client.post(reverse('plays:feedback'), data=feedback_data)
        self.assertEqual(Feedback.objects.count(), 1)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.comment, 'This is a valid feedback')
        self.assertEqual(feedback.username, self.user)
        self.assertEqual(response.status_code, 302)

    #a user who is not logged in tries to click on feedback nav bar but is redirected to the login page
    def test_not_logged_in_redirect(self):
        response = self.client.get(reverse('plays:feedback'))
        self.loginurl = reverse('plays:login')
        self.assertRedirects(response, f'{self.loginurl}?next={self.url}')


#submit comment

#submit rating

#chosen show


#logout
class LogOutTests(TestCase):
     def setUp(self):
        self.user = CustomUser.objects.create_user(username='usertest', password='userpassword', email='usertest@example.com', 
                                             first_name='john', last_name='doe')
        self.url = reverse('plays:shows')


def test_logout(self):
        self.client.login(username='usertest', password='userpassword')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.url)


#profile
class ProfileTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='usertest', password='userpassword', email='usertest@example.com', 
                                             first_name='john', last_name='doe')
        self.url = reverse('profile')

    #tests if a logged in user can update their bio    
    def test_update_bio(self):
        self.client.login(username="usertest", password="userpassword")
        response = self.client.post(self.url, json.dumps({"bio": "Updated bio"}), content_type="application/json")
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "Updated bio")
        self.assertRedirects(response, self.url)


    #tests if a logged in user can upload a profile picture
    def test_upload_profile_pic(self):
        self.client.login(username="usertest", password="userpassword")

        with open('test_image.jpg', 'wb') as f:
            f.write(b'Fake image content')  # Write some dummy content to the image file
        image = SimpleUploadedFile('profile_pic.jpg', open('test_image.jpg', 'rb').read(), content_type='image/jpeg')

        # Send a POST request with the image file
        response = self.client.post(reverse('profile'), {'profile_pic': image})
        # Refresh user from DB and check if profile picture is set
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile_pic)
        # Check that the response redirects
        self.assertRedirects(response, self.url)



    

