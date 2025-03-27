from django.test import TestCase, SimpleTestCase
from plays.models import CustomUser, Play, Category, Review

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

# Create your tests here.


#test the show page
class ShowsViewTest(TestCase):
    def setUp(self):
        # Set up some categories and plays
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

    def test_shows_view(self):
        response = self.client.get(reverse('plays:shows'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Play 1")
        self.assertContains(response, "Play 2")
        self.assertContains(response, "Play 3")



##test the different search functions too





#Testing views

#about view

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
class TestMapsPage(SimpleTestCase):
    def test_maps_page_status_code(self):
        # Test that the maps page returns status code 200
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
        

    def test_valid_login(self):
        response = self.client.post((reverse('login')), {'username': 'usertest', 'password':'userpassword'})
        self.assertRedirects(response, reverse('shows'))
        self.assertEqual(response.status_code, 302)

    def test_invalid_password(self):
        response = self.client.post('/login/', {'username' : 'usertest', 'password':'wrongpassword'})
        self.assertContains(response, 'Invalid login details supplied.')
        self.assertEqual(response.status_code, 200)

    def test_invalid_username(self):
        response = self.client.post('/login/', {'username' : 'wronguser', 'password':'userpassword'})
        self.assertContains(response, 'Invalid login details supplied.')
        self.assertEqual(response.status_code, 200)



 #signup tests   
class UserSignUpTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='usertest', password='userpassword', email='usertest@example.com', 
                                             first_name='john', last_name='doe')
        

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

#submit comment

#submit rating

#chosen show


#logout

#profile

#more signup


    

