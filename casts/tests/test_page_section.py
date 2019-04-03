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
