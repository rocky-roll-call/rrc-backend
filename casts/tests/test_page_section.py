from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Cast, PageSection


class PageSectionModelTestCase(TestCase):
    """
    Tests the PageSection model directly
    """

    def setUp(self):
        self.profile = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        ).profile
        self.cast = Cast.objects.create(name="Test Cast")
        self.ps1 = PageSection.objects.create(
            cast=self.cast, title="Test", text="This is a test"
        )
        self.ps2 = PageSection.objects.create(
            cast=self.cast,
            title="Another Test",
            text="This is a different test",
            order=2,
        )

    def test_details(self):
        """Check that features were created"""
        self.assertIsInstance(self.ps1.order, int)
        self.assertIsInstance(self.ps1.created_date, datetime)

    def test_ordering(self):
        """Tests ordering is preserved when fetching"""
        self.assertEqual(list(self.cast.page_sections.all()), [self.ps1, self.ps2])
        self.ps1.order = 3
        self.ps1.save()
        self.assertEqual(list(self.cast.page_sections.all()), [self.ps2, self.ps1])


class PageSectionAPITestCase(TestCase):
    """
    Test the PageSection API
    """

    def setUp(self):
        user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.profile = user.profile
        self.cast1 = Cast.objects.create(name="Test Cast")
        self.cast2 = Cast.objects.create(name="Another Cast")
        self.cast1.add_member(self.profile)
        self.cast1.add_manager(self.profile)
        self.ps1 = PageSection.objects.create(
            cast=self.cast1, title="Test", text="This is a test"
        )
        self.ps2 = PageSection.objects.create(
            cast=self.cast2,
            title="Another Test",
            text="This is a different test",
            order=2,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_list(self):
        """Tests calling page section list"""
        response = self.client.get(
            reverse("cast-page-sections", kwargs={"pk": self.cast1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.ps1.pk)

    def test_create(self):
        """Tests creating a new page section"""
        title, text = "Test", "This is a test"
        response = self.client.post(
            reverse("cast-page-sections", kwargs={"pk": self.cast1.pk}),
            {"title": title, "text": text},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        psection = PageSection.objects.get(id=response.data["id"])
        self.assertEqual(psection.title, title)
        self.assertEqual(psection.text, text)
        response = self.client.post(
            reverse("cast-page-sections", kwargs={"pk": self.cast2.pk}),
            {"title": title, "text": text},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        """Tests page section detail request"""
        response = self.client.get(
            reverse("cast-page-section", kwargs={"pk": self.ps1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("text", response.data)

    def test_update(self):
        """"Tests updating page section details"""
        self.assertEqual(self.ps1.title, "Test")
        title = "New Test"
        response = self.client.patch(
            reverse("cast-page-section", kwargs={"pk": self.ps1.id}),
            data={"title": title},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], title)
        psection = PageSection.objects.get(id=self.ps1.id)
        self.assertEqual(psection.title, title)
        # Prohibit updates to other casts' page sections
        response = self.client.patch(
            reverse("cast-page-section", kwargs={"pk": self.ps2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a manager can delete their page sections but not others"""
        response = self.client.delete(
            reverse("cast-page-section", kwargs={"pk": self.ps2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(
            reverse("cast-page-section", kwargs={"pk": self.ps1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(
            reverse("cast-page-section", kwargs={"pk": self.ps1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
