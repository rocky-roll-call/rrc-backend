# stdlib
from shutil import rmtree

# django
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# library
from rest_framework import status
from rest_framework.test import APIClient

# app
from ..models import Profile
from .test_user_photo import make_image


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
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.profile1 = user.profile
        self.profile2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        ).profile
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_list(self):
        """Tests calling profile list"""
        response = self.client.get(reverse("profiles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        """Tests user-based authentication on the requested object"""
        # User should have full access its own profile
        response = self.client.get(reverse("profile", kwargs={"pk": self.profile1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("show_email", response.data)
        # But a limitted view of others
        response = self.client.get(reverse("profile", kwargs={"pk": self.profile2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("show_email", response.data)

    def test_update(self):
        """"Tests that a user can update their own profile but not others"""
        self.assertEqual(self.profile1.bio, "")
        bio = "This is a test"
        response = self.client.patch(
            reverse("profile", kwargs={"pk": self.profile1.pk}), data={"bio": bio}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], bio)
        profile = Profile.objects.get(pk=self.profile1.pk)
        self.assertEqual(profile.bio, bio)

    def test_forbidden_update(self):
        """Prohibit updates to other users' profiles"""
        response = self.client.patch(
            reverse("profile", kwargs={"pk": self.profile2.pk}), data={"bio": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_image(self):
        """Tests updating a profile image"""
        self.assertEqual(self.profile1.image, "")
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            response = self.client.patch(
                reverse("profile", kwargs={"pk": self.profile1.pk}),
                {"image": data},
                format="multipart",
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["image"].endswith(".jpg"))
        self.assertIn("profile_image", response.data["image"])
        profile = Profile.objects.get(pk=self.profile1.pk)
        self.assertTrue(profile.image.path.endswith(".jpg"))
        self.assertIn("profile_image", profile.image.path)
        self.assertIn(self.profile1.user.username, profile.image.path)
