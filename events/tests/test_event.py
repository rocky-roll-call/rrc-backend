# stdlib
from datetime import datetime, timedelta

# django
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
