"""
Tests for moels.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_ceat_user_with_email_succesfull(self):
        email='test@gmail.com'
        password='dfgsc524DD'