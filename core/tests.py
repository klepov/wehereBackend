from django.test import TestCase, Client
from rest_framework import status

from core.views import reg, login
from .models import Parent
from rest_framework.test import APIRequestFactory, APIClient


class ParentTestCase(TestCase):

    def setUp(self):
        pass

    def test_parent(self):
        c = Client()
        response = reg(c.post("http://192.168.1.33:8080/whereiam/signup/",{'login':111,'password1':111,'password2':111}))
        self.assertRedirects(response,"http://192.168.1.33:8080/whereiam/")