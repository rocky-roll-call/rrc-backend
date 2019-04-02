from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Profile


class ProfileModelTestCase(TestCase):
    """
    Tests Profile models directly
    """

    def setUp(self):
        self.profile = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        ).profile

    def test_user_display_name(self):
        """Tests that the display name changes based on alt presence"""
        name, alt = "Test", "Not a Test"
        self.profile.name = name
        self.assertEqual(self.profile.display_name, name)
        self.profile.alt = alt
        self.assertEqual(self.profile.display_name, alt)


class ProfileAPITestCase(TestCase):
    """
    Test the Profile API
    """

    def setUp(self):
        user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.p1 = user.profile
        self.p2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        ).profile
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_retrieve(self):
        """Tests user-based authentication on the requested object"""
        # User should have full access its own profile
        response = self.client.get(reverse("profile", kwargs={"pk": self.p1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("show_email", response.data)
        # But a limitted view of others
        response = self.client.get(reverse("profile", kwargs={"pk": self.p2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("show_email", response.data)

    def test_update(self):
        """"Tests that a user can update their own profile but not others"""
        self.assertEqual(self.p1.bio, "")
        bio = "This is a test"
        response = self.client.patch(
            reverse("profile", kwargs={"pk": self.p1.id}), data={"bio": bio}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], bio)
        profile = Profile.objects.get(id=self.p1.id)
        self.assertEqual(profile.bio, bio)
        # Check for unauth when updating other profiles
        response = self.client.patch(
            reverse("profile", kwargs={"pk": self.p2.id}), data={"bio": bio}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
