"""
Tests for models
"""

from django.test import TestCase

# get default user model for the project configured in settings
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        # .objects is a reference to the manager we are going to create
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        # check password through our hashong system
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalzied(self):
        "Test email is normalized for new users"
        sample_emails = [
            ["TEST1@eXample.coM", "TEST1@example.com"],
            ["Test2@EXample.cOm", "Test2@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "samplepass123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test crating a user without an email raises an error"""
        # create user raisees exception if empty email
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpassword123")

    def test_create_superuser(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser("test@example.com", "test123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
