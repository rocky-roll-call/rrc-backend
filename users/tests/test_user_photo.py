from datetime import datetime
from tempfile import NamedTemporaryFile
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import UserPhoto


def make_image() -> NamedTemporaryFile:
    image = Image.new("RGB", (100, 100))
    tmp_file = NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file)
    return tmp_file


class UserPhotoModelTestCase(TestCase):
    """
    Tests UserPhoto models directly
    """

    def setUp(self):
        self.profile = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        ).profile
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo = UserPhoto.objects.create(profile=self.profile)
            self.photo.image = ImageFile(data, tmpim.name)

    def test_photo_details(self):
        """Tests image field return types"""
        self.assertIsInstance(self.photo.created_date, datetime)
        self.assertTrue(self.photo.image.url.endswith(".jpg"))


class UserPhotoAPITestCase(TestCase):
    """
    Test the UserPhoto API
    """

    def setUp(self):
        user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.p1 = user.profile
        self.p2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        ).profile
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo1 = UserPhoto.objects.create(profile=self.p1)
            self.photo1.image = ImageFile(data, tmpim.name)
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo2 = UserPhoto.objects.create(profile=self.p2)
            self.photo2.image = ImageFile(data, tmpim.name)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_list(self):
        response = self.client.get(reverse("profile-photos", kwargs={"pk": self.p1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.photo1.pk)

    def test_create(self):
        """Tests creating a new user photo"""
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            response = self.client.post(
                reverse("profile-photos", kwargs={"pk": self.p1.pk}),
                {"image": data, "description": "Test Image"},
                format="multipart",
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        photo = UserPhoto.objects.get(id=response.data["id"])
        fname = tmpim.name.split("/")[-1]
        self.assertIn(fname, photo.image.path)
        self.assertIn(self.p1.user.username, photo.image.path)

    def test_retrieve(self):
        """Tests photo detail request"""
        response = self.client.get(
            reverse("profile-photo", kwargs={"pk": self.photo1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image", response.data)

    def test_update(self):
        """"Tests updating photo details"""
        self.assertEqual(self.photo1.description, "")
        desc = "This is a test"
        response = self.client.patch(
            reverse("profile-photo", kwargs={"pk": self.photo1.id}),
            data={"description": desc},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], desc)
        profile = UserPhoto.objects.get(id=self.photo1.id)
        self.assertEqual(profile.description, desc)
        # Prohibit updates to other users' photos
        response = self.client.patch(
            reverse("profile-photo", kwargs={"pk": self.photo2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a user can delete their own photos but not others"""
        response = self.client.delete(
            reverse("profile-photo", kwargs={"pk": self.photo2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(
            reverse("profile-photo", kwargs={"pk": self.photo1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(
            reverse("profile-photo", kwargs={"pk": self.photo1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)