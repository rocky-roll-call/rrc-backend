# stdlib
from datetime import datetime
from shutil import rmtree

# django
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.test import TestCase
from django.urls import reverse

# library
from rest_framework import status
from rest_framework.test import APIClient

# app
from users.tests.test_user_photo import make_image
from ..models import Cast, CastPhoto


class CastPhotoModelTestCase(TestCase):
    """
    Tests CastPhoto models directly
    """

    def setUp(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        self.cast = Cast.objects.create(name="Test Cast")
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo = CastPhoto.objects.create(cast=self.cast)
            self.photo.image = ImageFile(data, tmpim.name)

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_photo_details(self):
        """Tests image field return types"""
        self.assertIsInstance(self.photo.created_date, datetime)
        self.assertTrue(self.photo.image.url.endswith(".jpg"))


class CastPhotoAPITestCase(TestCase):
    """
    Test the CastPhoto API
    """

    def setUp(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.profile = user.profile
        self.cast1 = Cast.objects.create(name="Test Cast")
        self.cast2 = Cast.objects.create(name="Another Cast")
        self.cast1.add_member(self.profile)
        self.cast1.add_manager(self.profile)
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo1 = CastPhoto.objects.create(cast=self.cast1)
            self.photo1.image = ImageFile(data, tmpim.name)
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo2 = CastPhoto.objects.create(cast=self.cast1)
            self.photo2.image = ImageFile(data, tmpim.name)
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            self.photo3 = CastPhoto.objects.create(cast=self.cast2)
            self.photo3.image = ImageFile(data, tmpim.name)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_list(self):
        """Tests calling cast photo list"""
        response = self.client.get(reverse("cast-photos", kwargs={"pk": self.cast1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Photos are reverse ordered
        self.assertEqual(response.data[0]["id"], self.photo2.pk)

    def test_create(self):
        """Tests creating a new cast photo"""
        tmpim = make_image()
        with open(tmpim.name, "rb") as data:
            response = self.client.post(
                reverse("cast-photos", kwargs={"pk": self.cast1.pk}),
                {"image": data, "description": "Test Image"},
                format="multipart",
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        photo = CastPhoto.objects.get(id=response.data["id"])
        fname = tmpim.name.split("/")[-1]
        self.assertIn(fname, photo.image.path)
        self.assertIn(self.cast1.slug, photo.image.path)
        # Prevent non-managers from adding photos
        with open(tmpim.name, "rb") as data:
            response = self.client.post(
                reverse("cast-photos", kwargs={"pk": self.cast2.pk}),
                {"image": data, "description": "Test Image"},
                format="multipart",
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        """Tests photo detail request"""
        response = self.client.get(reverse("cast-photo", kwargs={"pk": self.photo1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image", response.data)

    def test_update(self):
        """"Tests updating photo details"""
        self.assertEqual(self.photo1.description, "")
        desc = "This is a test"
        response = self.client.patch(
            reverse("cast-photo", kwargs={"pk": self.photo1.id}),
            data={"description": desc},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], desc)
        photo = CastPhoto.objects.get(id=self.photo1.id)
        self.assertEqual(photo.description, desc)
        # Prohibit updates to other casts' photos
        response = self.client.patch(
            reverse("cast-photo", kwargs={"pk": self.photo3.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a manager can delete their cast photos but not others"""
        response = self.client.delete(
            reverse("cast-photo", kwargs={"pk": self.photo3.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(
            reverse("cast-photo", kwargs={"pk": self.photo1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(
            reverse("cast-photo", kwargs={"pk": self.photo1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
