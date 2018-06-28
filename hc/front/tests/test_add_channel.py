from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ### Test that the team access works
    def test_team_access_for_channel(self):
        #login with alice and create a channel
        self.client.login(username="alice@example.org", password="password")
        add_channel = Channel(user=self.alice, kind="slack")
        add_channel.save()
         
        #login with bob to see if he can delete the same channel alice created
        self.client.login(username="bob@example.org", password="password")
        url = "/integrations/%s/remove/" % add_channel.code
        r = self.client.post(url)
        self.assertEqual(r.status_code, 302)

    ### Test that bad kinds don't work
    def test_bad_kinds_not_working(self):
        """ Test that bad intergration kinds are not working """
        self.client.login(username="alice@example.com", password="password")
        bad_kinds = ("instagram", "snapchat", "heroku", "github")
        for kind in bad_kinds:
            url = "/intergrations/add_%s" % kind
            r = self.client.get(url)
            assert r.status_code == 404
