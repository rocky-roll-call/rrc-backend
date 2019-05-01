# django
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

# library
from rest_framework import status
from rest_framework.test import APIClient


class RegistrationTestCase(TestCase):
    """
    Tests new user registration
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.password = "mysupersecrettestpasswordomgyouguys321"
        self.client = APIClient()
        # NOTE: not authenticated

    def test_registration(self):
        """
        Tests new user creation and email verification
        """
        username, email = "tester", "tester@test.io"
        response = self.client.post(
            reverse("rest_register"),
            {
                "username": username,
                "email": email,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        data = response.data["user"]
        self.assertIn("pk", data)
        pk = data["pk"]
        self.assertEqual(data["username"], username)
        self.assertEqual(data["email"], email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(User.objects.all()), 2)
        # Verify email
        key = mail.outbox[0].body
        key = key[key.find("account-confirm-email") :].split("/")[1]
        response = self.client.post(reverse("rest_verify_email"), {"key": key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "ok")
        user = User.objects.get(pk=pk)
        self.assertTrue(user.emailaddress_set.all()[0].verified)

    def test_bad_password(self):
        """
        Registration should return an error reason for bad passwords
        """
        username, email = "tester", "tester@test.io"
        for password in ("short", "testing", "123", "qwerty"):
            response = self.client.post(
                reverse("rest_register"),
                {
                    "username": username,
                    "email": email,
                    "password1": password,
                    "password2": password,
                },
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("password1", response.data)

    def test_mismatched_password(self):
        """
        Submitted password fields must match
        """
        response = self.client.post(
            reverse("rest_register"),
            {
                "username": "tester",
                "email": "tester@test.io",
                "password1": self.password,
                "password2": self.password + "nope",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_existing_username(self):
        """
        Cannot register an existing username
        """
        response = self.client.post(
            reverse("rest_register"),
            {
                "username": self.user.username,
                "email": "tester@test.io",
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_existing_email(self):
        """
        Cannot register an existing email
        """
        response = self.client.post(
            reverse("rest_register"),
            {
                "username": "tester",
                "email": self.user.email,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_bad_verification_code(self):
        """
        Should receive error for non-existant verification key
        """
        response = self.client.post(reverse("rest_verify_email"), {"key": "M"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
