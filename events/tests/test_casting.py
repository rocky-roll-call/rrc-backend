# stdlib
from datetime import timedelta

# django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# library
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

# app
from casts.models import Cast
from events.models import Casting, Event


class TestCastingModelTestCase(TestCase):
    """
    Tests the Casting model directly
    """

    def setUp(self):
        self.profile = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        ).profile
        profile2 = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        ).profile
        cast1 = Cast.objects.create(name="Test Cast")
        cast2 = Cast.objects.create(name="Another Cast")
        cast1.add_member(self.profile)
        cast1.add_manager(self.profile)
        cast2.add_member(profile2)
        start = timezone.now()
        self.event = Event.objects.create(
            name="Test Event",
            cast=cast1,
            description="A test event",
            venue="A place",
            start=start + timedelta(days=1),
        )
        event2 = Event.objects.create(
            name="Another Event",
            cast=cast2,
            description="Another test event",
            venue="Another place",
            start=start + timedelta(days=1),
        )
        self.casting1 = Casting.objects.create(
            event=self.event, role=Casting.EMCEE, writein="notamember"
        )
        self.casting2 = Casting.objects.create(
            event=self.event, profile=self.profile, role=Casting.FRANK
        )
        self.casting3 = Casting.objects.create(
            event=event2, profile=profile2, role=Casting.RIFF
        )

    def test_details(self):
        """Check that features were created"""
        self.assertTrue(self.casting2.show_picture)
        self.assertFalse(self.casting1.show_picture)
        self.assertEqual(self.casting1.role, 20)
        self.assertEqual(self.casting1.get_role_display(), "Emcee")

    def test_order(self):
        """Tests that castings are ordered by role"""
        castings = list(self.event.castings.all())
        self.assertEqual(castings, [self.casting2, self.casting1])

    def test_bad_init(self):
        """Tests error raised when giving bad profile and writein values"""
        with self.assertRaises(ValidationError):
            Casting.objects.create(event=self.event, role=Casting.FRANK)
        with self.assertRaises(ValidationError):
            Casting.objects.create(
                event=self.event,
                role=Casting.FRANK,
                profile=self.profile,
                writein="test",
            )


class CastingAPITestCase(TestCase):
    """
    Test the Casting API
    """

    def setUp(self):
        user = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        )
        self.profile1 = user.profile
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
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_options(self):
        """Tests choice info found in options method"""
        response = self.client.options(
            reverse("castings", kwargs={"pk": self.event1.pk})
        )
        self.assertIn("choices", response.data["actions"]["POST"]["role"])

    def test_list(self):
        """Tests calling casting list"""
        response = self.client.get(reverse("castings", kwargs={"pk": self.event1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_profile(self):
        """Tests creating a new casting with a profile"""
        response = self.client.post(
            reverse("castings", kwargs={"pk": self.event1.pk}),
            {"profile": self.profile1.pk, "role": Casting.FRANK},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        casting = Casting.objects.get(pk=response.data["id"])
        self.assertEqual(casting.event, self.event1)
        self.assertEqual(casting.profile, self.profile1)
        self.assertEqual(casting.role, Casting.FRANK)
        self.assertEqual(casting.role_name, "Dr. Frank-N-Furter")
        self.assertTrue(casting.show_picture)
        self.assertIsNone(casting.writein)

    def test_create_writein(self):
        """Tests creating a new casting with a write-in"""
        name = "Test"
        response = self.client.post(
            reverse("castings", kwargs={"pk": self.event1.pk}),
            {"writein": name, "role": Casting.EMCEE},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        casting = Casting.objects.get(pk=response.data["id"])
        self.assertEqual(casting.event, self.event1)
        self.assertIsNone(casting.profile)
        self.assertEqual(casting.role, Casting.EMCEE)
        self.assertEqual(casting.role_name, "Emcee")
        self.assertFalse(casting.show_picture)
        self.assertEqual(casting.writein, name)

    def test_bad_create(self):
        """Tests fail response when giving bad data"""
        # No profile or write-in
        response = self.client.post(
            reverse("castings", kwargs={"pk": self.event1.pk}), {"role": Casting.EMCEE}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Both profile and write-in
        response = self.client.post(
            reverse("castings", kwargs={"pk": self.event1.pk}),
            {"profile": self.profile1.pk, "role": Casting.FRANK, "writein": "test"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Profile not a member
        response = self.client.post(
            reverse("castings", kwargs={"pk": self.event1.pk}),
            {"profile": self.profile2.pk, "role": Casting.FRANK},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forbidden_create(self):
        """Prohibit creating castings for events on non-managed casts"""
        response = self.client.post(
            reverse("castings", kwargs={"pk": self.event2.pk}),
            {"profile": self.profile1.pk, "role": Casting.FRANK},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        """Tests casting detail request"""
        response = self.client.get(reverse("casting", kwargs={"pk": self.casting2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("role", response.data)
        self.assertIsInstance(response.data["role"], int)
        self.assertEqual(response.data["role_name"], "Dr. Frank-N-Furter")
        self.assertTrue(response.data["show_picture"])

    def test_update(self):
        """"Tests updating casting details"""
        self.assertEqual(self.casting1.role, Casting.EMCEE)
        role = Casting.RIFF
        response = self.client.patch(
            reverse("casting", kwargs={"pk": self.casting1.pk}), data={"role": role}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], role)
        casting = Casting.objects.get(pk=self.casting1.pk)
        self.assertEqual(casting.role, role)

    def test_forbidden_update(self):
        """Prohibit updates to other cast events"""
        response = self.client.patch(
            reverse("casting", kwargs={"pk": self.casting3.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a cast manager can delete castings"""
        response = self.client.delete(
            reverse("casting", kwargs={"pk": self.casting1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(
            reverse("casting", kwargs={"pk": self.casting1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forbidden_delete(self):
        """Tests that a user can't delete a casting of a non-managed cast"""
        response = self.client.delete(
            reverse("casting", kwargs={"pk": self.casting3.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
