from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta 
from django.utils import timezone

class UnresolvedChecksTest(BaseTestCase):

    def setUp(self):
        super(UnresolvedChecksTest, self).setUp()
        self.check = Check(user=self.alice, name='Failing Check')
        self.check.save()

    def test_unresolved_checks_works(self):
        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/unresolved/")
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_unresolved_check(self):
        self.client.login(username="alice@example.org", password="password")
        self.check.last_ping = timezone.now() - timedelta(days=3)
        self.check.status = "up"
        self.check.save()
        self.check.refresh_from_db()
        response = self.client.get("/unresolved/")
        self.assertIn("Failing Check", response)
