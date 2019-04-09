# stdlib
from datetime import datetime, timedelta

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
from events.models import Casting, Event, get_upcoming_events


class EventModelTestCase(TestCase):
    """
    Tests the Event model directly
    """

    def setUp(self):
        self.cast1 = Cast.objects.create(name="Test Cast")
        self.cast2 = Cast.objects.create(name="Another Cast")
        start = timezone.now()
        self.event1 = Event.objects.create(
            name="Test Event",
            cast=self.cast1,
            description="A test event",
            venue="A place",
            start=start + timedelta(days=2),
        )
        self.event2 = Event.objects.create(
            name="Another Event",
            cast=self.cast1,
            description="Another test event",
            venue="Another place",
            start=start,
        )
        self.event3 = Event.objects.create(
            name="A Different Event",
            cast=self.cast2,
            description="A differenttest event",
            venue="A different place",
            start=start + timedelta(days=1),
        )

    def test_details(self):
        """Check that features were created"""
        self.assertFalse(self.event1.is_expired)
        self.assertIsInstance(self.event1.created, datetime)

    def test_order(self):
        """Tests that events are always ordered by start timestamp"""
        events = list(Event.objects.all())
        self.assertEqual(events, [self.event2, self.event3, self.event1])
        self.assertEqual(list(self.cast1.events.all()), [self.event2, self.event1])
        self.assertEqual(list(self.cast2.events.all()), [self.event3])

    def _validate_calendar_event(self, calendar: {str: [Event]}, event: Event):
        key = event.start.strftime(r"%Y-%m-%d")
        self.assertIn(key, calendar)
        self.assertEqual(calendar[key][0], event)

    def test_upcoming_events(self):
        """Tests upcoming events function"""
        calendar = get_upcoming_events()
        for event in (self.event1, self.event3):
            self._validate_calendar_event(calendar, event)
        calendar = get_upcoming_events(days=1)
        self._validate_calendar_event(calendar, self.event3)
        calendar = get_upcoming_events(cast=self.cast2.pk)
        self._validate_calendar_event(calendar, self.event3)

    def test_cast_events(self):
        """Tests future events from a Cast object"""
        self.assertEqual(list(self.cast1.future_events), [self.event1])
        self.assertEqual(list(self.cast2.future_events), [self.event3])


class EventAPITestCase(TestCase):
    """
    Test the Cast API
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
        start = timezone.now()
        self.event1 = Event.objects.create(
            name="Test Event",
            cast=self.cast1,
            description="A test event",
            venue="A place",
            start=start + timedelta(days=2),
        )
        self.event2 = Event.objects.create(
            name="Another Event",
            cast=self.cast1,
            description="Another test event",
            venue="Another place",
            start=start,
        )
        self.event3 = Event.objects.create(
            name="A Different Event",
            cast=self.cast2,
            description="A differenttest event",
            venue="A different place",
            start=start + timedelta(days=1),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_list(self):
        """Tests calling event list"""
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create(self):
        """Tests creating a new event"""
        name, desc, venue = "New Event", "A new event", "A new place"
        start = timezone.now() + timedelta(days=1)
        response = self.client.post(
            reverse("events"),
            {
                "name": name,
                "description": desc,
                "venue": venue,
                "start": start,
                "cast": self.cast1.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = Event.objects.get(pk=response.data["id"])
        self.assertEqual(event.name, name)
        self.assertEqual(event.description, desc)
        self.assertEqual(event.venue, venue)
        self.assertEqual(event.start, start)
        self.assertEqual(event.cast, self.cast1)

    def test_forbidden_create(self):
        """Prohibit creating events for non-managed casts"""
        response = self.client.post(
            reverse("events"),
            {
                "name": "test",
                "description": "test",
                "venue": "test",
                "start": timezone.now(),
                "cast": self.cast2.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        """Tests event detail request"""
        response = self.client.get(reverse("event", kwargs={"pk": self.event1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)

    def test_update(self):
        """"Tests updating event details"""
        self.assertEqual(self.event1.name, "Test Event")
        name = "Updated Event"
        response = self.client.patch(
            reverse("cast", kwargs={"pk": self.cast1.pk}), data={"name": name}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], name)
        event = Event.objects.get(pk=self.event1.pk)
        self.assertEqual(event.name, name)

    def test_forbidden_update(self):
        """Prohibit updates to other casts"""
        response = self.client.patch(reverse("event", kwargs={"pk": self.event3.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a cast manager can delete events"""
        response = self.client.delete(reverse("event", kwargs={"pk": self.event1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse("event", kwargs={"pk": self.event1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forbidden_delete(self):
        """Tests that a user can't delete an event of a non-managed cast"""
        response = self.client.delete(reverse("event", kwargs={"pk": self.event3.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
