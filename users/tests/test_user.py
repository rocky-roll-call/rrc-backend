from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserModelTestCase(TestCase):
    """
    Tests the auth.User model directly
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )

    def test_profile_creation(self):
        """Tests that a profile was created for the user"""
        self.assertIsNotNone(self.user.profile)


class UserAPITestCase(TestCase):
    """
    Tests the User API
    """

    def setUp(self):
        self.u1 = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.u2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.u1)

    def test_list(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        """Tests user-based authentication on the requested object"""
        # User should be able to access its own instance
        response = self.client.get(reverse("user", kwargs={"pk": self.u1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # But not those of others
        response = self.client.get(reverse("user", kwargs={"pk": self.u2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
