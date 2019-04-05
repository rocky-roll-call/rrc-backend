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

    def test_member_add_removes_request(self):
        """Tests adding a member removes an existing request"""
        self.cast.add_member_request(self.profile)
        self.assertTrue(self.cast.has_requested_membership(self.profile))
        self.assertFalse(self.cast.is_member(self.profile))
        self.cast.add_member(self.profile)
        self.assertTrue(self.cast.is_member(self.profile))
        self.assertFalse(self.cast.has_requested_membership(self.profile))

    def test_member_add_if_blocked(self):
        """Can't add member if blocked"""
        self.cast.block_user(self.profile)
        self.assertTrue(self.cast.is_blocked(self.profile))
        with self.assertRaises(ValueError):
            self.cast.add_member(self.profile)
        self.assertFalse(self.cast.is_member(self.profile))
        self.assertTrue(self.cast.is_blocked(self.profile))
        self.cast.unblock_user(self.profile)

    def test_member_remove_if_manager(self):
        """Cannot remove member if a manager"""
        self.cast.add_member(self.profile)
        self.cast.add_manager(self.profile)
        self.assertTrue(self.cast.is_manager(self.profile))
        with self.assertRaises(ValueError):
            self.cast.remove_member(self.profile)
        self.assertTrue(self.cast.is_manager(self.profile))
        self.cast.remove_manager(self.profile)
        self.cast.remove_member(self.profile)

    def test_requests(self):
        """Tests membership request lifecycle"""
        self._add_check_remove(
            self.cast.add_member_request,
            self.cast.has_requested_membership,
            self.cast.remove_member_request,
        )

    def test_request_if_member(self):
        """Can't request if already a member"""
        self.cast.add_member(self.profile)
        self.assertTrue(self.cast.is_member(self.profile))
        with self.assertRaises(ValueError):
            self.cast.add_member_request(self.profile)
        self.assertFalse(self.cast.has_requested_membership(self.profile))
        self.cast.remove_member(self.profile)

    def test_request_if_blocked(self):
        """Can't request if blocked"""
        self.cast.block_user(self.profile)
        self.assertFalse(self.cast.has_requested_membership(self.profile))
        with self.assertRaises(ValueError):
            self.cast.add_member_request(self.profile)
        self.assertFalse(self.cast.has_requested_membership(self.profile))
        self.cast.unblock_user(self.profile)

    def test_blocked(self):
        """Tests blocked user lifecycle"""
        self._add_check_remove(
            self.cast.block_user, self.cast.is_blocked, self.cast.unblock_user
        )

    def test_block_if_manager(self):
        """Can't block a manager"""
        self.cast.add_member(self.profile)
        self.cast.add_manager(self.profile)
        self.assertTrue(self.cast.is_manager(self.profile))
        with self.assertRaises(ValueError):
            self.cast.block_user(self.profile)
        self.assertFalse(self.cast.is_blocked(self.profile))
        self.assertTrue(self.cast.is_manager(self.profile))
        self.cast.remove_manager(self.profile)
        self.cast.remove_member(self.profile)

    def test_block_removes_members(self):
        """Blocking an existing member should remove them"""
        self.cast.add_member(self.profile)
        self.assertTrue(self.cast.is_member(self.profile))
        self.cast.block_user(self.profile)
        self.assertTrue(self.cast.is_blocked(self.profile))
        self.assertFalse(self.cast.is_member(self.profile))


class CastAPITestCase(TestCase):
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
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_list(self):
        """Tests calling cast list"""
        response = self.client.get(reverse("casts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        """Tests creating a new cast"""
        name, desc, email = "New Cast", "A new cast", "test@cast.io"
        response = self.client.post(
            reverse("casts"), {"name": name, "description": desc, "email": email}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cast = Cast.objects.get(id=response.data["id"])
        self.assertEqual(cast.name, name)
        self.assertEqual(cast.description, desc)
        self.assertEqual(cast.email, email)
        self.assertEqual(cast.slug, "new-cast")
        self.assertTrue(cast.is_member(self.profile))
        self.assertTrue(cast.is_manager(self.profile))
        # Test unique name
        response = self.client.post(reverse("casts"), {"name": self.cast1.name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        """Tests cast detail request"""
        response = self.client.get(reverse("cast", kwargs={"pk": self.cast1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)

    def test_update(self):
        """"Tests updating cast details"""
        self.assertEqual(self.cast1.name, "Test Cast")
        name, slug = "Updated Cast", "updated-cast"
        response = self.client.patch(
            reverse("cast", kwargs={"pk": self.cast1.id}), data={"name": name}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], name)
        self.assertEqual(response.data["slug"], slug)
        cast = Cast.objects.get(id=self.cast1.id)
        self.assertEqual(cast.name, name)
        self.assertEqual(cast.slug, slug)
        # Prohibit updates to other casts
        response = self.client.patch(reverse("cast", kwargs={"pk": self.cast2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """Tests that a manager can delete their casts but not others"""
        response = self.client.delete(reverse("cast", kwargs={"pk": self.cast2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Delete should fail if the cast has more than one manager
        profile = User.objects.create_user(
            username="mctest", email="mctest@test.io", password="testing mctest"
        ).profile
        self.cast1.add_member(profile)
        self.cast1.add_manager(profile)
        response = self.client.delete(reverse("cast", kwargs={"pk": self.cast1.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.cast1.remove_manager(profile)
        response = self.client.delete(reverse("cast", kwargs={"pk": self.cast1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse("cast", kwargs={"pk": self.cast1.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CastListAPITestCase(TestCase):
    """
    Test the Cast API
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
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def _list_add_check_remove(self, url_name: str, fcheck: str):
        """Tests list endpoint's add, check, remove, and dne events"""
        url = reverse(url_name, kwargs={"pk": self.cast1.pk, "pid": self.profile2.pk})
        # Cannot remove non-added profile
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(getattr(self.cast1, fcheck)(self.profile2))
        # Add profile
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(getattr(self.cast1, fcheck)(self.profile2))
        # Cannot re-add profile
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Remove profile
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(getattr(self.cast1, fcheck)(self.profile2))
        # Bad cast
        response = self.client.delete(
            reverse(url_name, kwargs={"pk": 0, "pid": self.profile2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Bad profile
        response = self.client.delete(
            reverse(url_name, kwargs={"pk": self.cast1.pk, "pid": 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Not allowed for other casts
        response = self.client.post(
            reverse(url_name, kwargs={"pk": self.cast2.pk, "pid": self.profile2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_list(self):
        """Tests member add/remove endpoint"""
        self._list_add_check_remove("cast-member", "is_member")

    def test_manager_list(self):
        """Tests member add/remove endpoint"""
        # Cannot add a non-member
        response = self.client.post(
            reverse(
                "cast-manager", kwargs={"pk": self.cast1.pk, "pid": self.profile2.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.cast1.add_member(self.profile2)
        self._list_add_check_remove("cast-manager", "is_manager")

    def test_request_list(self):
        """"""
        self._list_add_check_remove("cast-member-request", "has_requested_membership")

    def test_blocked_list(self):
        """"""
        self._list_add_check_remove("cast-blocked", "is_blocked")
