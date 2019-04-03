from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Cast


class CastModelTestCase(TestCase):
    """
    Tests the Cast model directly
    """

    def setUp(self):
        self.profile = User.objects.create_user(
            username="test", email="test@test.io", password="testing"
        ).profile
        self.cast = Cast.objects.create(name="Test Cast")

    def test_details(self):
        """Check that features were created"""
        self.assertEqual(self.cast.slug, "test-cast")
        self.assertIsInstance(self.cast.created_date, datetime)
        self.assertIsInstance(self.cast.modified_date, datetime)

    def _add_check_remove(self, fadd, fcheck, fremv):
        """Runs lifecycle checks on a user"""
        self.assertFalse(fcheck(self.profile))
        fadd(self.profile)
        self.assertTrue(fcheck(self.profile))
        with self.assertRaises(ValueError):
            fadd(self.profile)
        fremv(self.profile)
        self.assertFalse(fcheck(self.profile))
        with self.assertRaises(ValueError):
            fremv(self.profile)

    def test_managers(self):
        """Tests manager lifecycle"""
        # Requires membership first
        with self.assertRaises(ValueError):
            self.cast.add_manager(self.profile)
        self.cast.add_member(self.profile)
        self._add_check_remove(
            self.cast.add_manager, self.cast.is_manager, self.cast.remove_manager
        )
        self.cast.remove_member(self.profile)

    def test_members(self):
        """Tests membership lifecycle"""
        self._add_check_remove(
            self.cast.add_member, self.cast.is_member, self.cast.remove_member
        )

    def test_requests(self):
        """Tests membership request lifecycle"""
        self._add_check_remove(
            self.cast.add_member_request,
            self.cast.has_requested_membership,
            self.cast.remove_member_request,
        )

    def test_blocked(self):
        """Tests blocked user lifecycle"""
        self._add_check_remove(
            self.cast.block_user, self.cast.is_blocked, self.cast.unblock_user
        )
