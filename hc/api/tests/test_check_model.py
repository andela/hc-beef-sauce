from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


class CheckModelTestCase(TestCase):

    def test_it_strips_tags(self):
        """Tests if tags are stripped"""
        check = Check()
        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])
        check1 = Check()
        check1.tags = ""
        self.assertEquals(check1.tags_list(), [])

    def test_status_works_with_grace_period(self):
        """Test status works if check is in grace period"""
        check = Check()
        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())
        self.assertEqual(check.get_status(), "up")

    def test_paused_check_is_not_in_grace_period(self):
        """Test paused check not in grace period"""
        check = Check()
        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())
        check.status = "paused"
        self.assertFalse(check.in_grace_period())

    def test_new_check_not_in_grace_period(self):
        """Test new check not in grace period"""
        check = Check(name="New Check")
        self.assertFalse(check.in_grace_period())
