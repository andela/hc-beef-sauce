from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_checks_team_access(self):
        """Test if team access works on checks"""
        #add check with alice
        self.client.login(username="alice@example.org", password="password")
        add_check = Check(user=self.alice)
        add_check.save()

        #check if bob can access logs for the created check
        url = "/checks/%s/log/" % add_check.code
        self.client.login(username="bob@example.org", password="password")
        r = self.client.get(url)
        assert r.status_code == 200
