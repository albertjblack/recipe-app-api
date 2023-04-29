"""
Tests for the django admin modifications
"""

from django.test import (
    TestCase,
    Client,
)
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSitesTests(TestCase):
    """Tests for django admin"""

    # setup modules .. run before every test we add
    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
        )
        # request forced to user admin_user
        self.client.force_login(self.admin_user)

        # test user
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="tespass123", name="Test User"
        )

    def test_user_list(self):
        """Test that users are listed on page"""
        # reverse to GET the URL for the changelist inside django admin .. Determine Url
        url = reverse("admin:core_user_changelist")
        # authenticated as the admin user
        res = self.client.get(url)

        # check page contains name and email of the test user created
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_admin_user_page(self):
        """Test the create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
