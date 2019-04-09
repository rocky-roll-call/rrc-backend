from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Profile


class UserModelTestCase(TestCase):
    """
    Tests the auth.User model directly
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )

    def test_profile_lifecycle(self):
        """Tests that a profile was created/destroyed for the user"""
        self.assertIsNotNone(self.user.profile)
        pk = self.user.profile.pk
        self.assertIsNotNone(Profile.objects.get(pk=pk))
        self.user.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(pk=pk)


class UserAPITestCase(TestCase):
    """
    Tests the User API
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.user2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_list(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_auth(self):
        """Tests user-based authentication on the requested object"""
        # User should be able to access its own instance
        response = self.client.get(reverse("user", kwargs={"pk": self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # But not those of others
        response = self.client.get(reverse("user", kwargs={"pk": self.user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        """"Tests that a user can update their own details but not others"""
        old_email, new_email = "test@test.io", "notatest@test.io"
        self.assertEqual(self.user1.email, old_email)
        response = self.client.patch(
            reverse("user", kwargs={"pk": self.user1.pk}), data={"email": new_email}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], new_email)
        user = User.objects.get(pk=self.user1.pk)
        self.assertEqual(user.email, new_email)

    def test_forbidden_update(self):
        """Prohibit updates to other users' models"""
        response = self.client.patch(
            reverse("user", kwargs={"pk": self.user2.pk}), data={"email": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a user can delete their own model but not others"""
        response = self.client.delete(reverse("user", kwargs={"pk": self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse("user", kwargs={"pk": self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forbidden_delete(self):
        """Tests that a user can't delete another user"""
        response = self.client.delete(reverse("user", kwargs={"pk": self.user2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
