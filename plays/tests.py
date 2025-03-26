from django.test import TestCase, SimpleTestCase
from plays.models import CustomUser

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

#Testing views

class TestAboutPage(SimpleTestCase):
    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code,200)

    def test_about_page_correct_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'plays/about.html')




    #populates stuff
    


    

