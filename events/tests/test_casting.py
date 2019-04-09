# stdlib
from datetime import timedelta

# django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# library
from rest_framework import status
from rest_framework.test import APIClient

# app
from casts.models import Cast
from events.models import Casting, Event


class CastingModelTestCase(TestCase):
    """
    Tests the Casting model directly
    """

    def setUp(self):
        self.profile1 = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        ).profile
        self.profile2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        ).profile
        self.cast1 = Cast.objects.create(name="Test Cast")
        self.cast2 = Cast.objects.create(name="Another Cast")
        self.cast1.add_member(self.profile1)
        self.cast1.add_manager(self.profile1)
        self.cast2.add_member(self.profile2)
        start = timezone.now()
        self.event1 = Event.objects.create(
            name="Test Event",
            cast=self.cast1,
            description="A test event",
            venue="A place",
            start=start + timedelta(days=1),
        )
        self.event2 = Event.objects.create(
            name="Another Event",
            cast=self.cast2,
            description="Another test event",
            venue="Another place",
            start=start + timedelta(days=1),
        )
        self.casting1 = Casting.objects.create(
            event=self.event1, role=Casting.EMCEE, writein="notamember"
        )
        self.casting2 = Casting.objects.create(
            event=self.event1, profile=self.profile1, role=Casting.FRANK
        )
        self.casting3 = Casting.objects.create(
            event=self.event2, profile=self.profile2, role=Casting.RIFF
        )

    def test_details(self):
        """Check that features were created"""
        self.assertTrue(self.casting2.show_picture)
        self.assertFalse(self.casting1.show_picture)
        self.assertEqual(self.casting1.role, 20)
        self.assertEqual(self.casting1.get_role_display(), "Emcee")

    def test_order(self):
        """Tests that castings are ordered by role"""
        castings = list(self.event1.castings.all())
        self.assertEqual(castings, [self.casting2, self.casting1])
