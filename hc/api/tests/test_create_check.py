import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None, HTTP_X_API_KEY=""):
        if HTTP_X_API_KEY != "":
            r = self.client.post(self.URL, json.dumps(data),
                                content_type="application/json",
                                HTTP_X_API_KEY=HTTP_X_API_KEY)
        else:
            r = self.client.post(self.URL, json.dumps(data),
                                content_type="application/json")

        if expected_error:
            doc = r.json()
            self.assertEqual(r.status_code, 400)

            error_msgs = [
                "timeout is not a number",
                "name is not a string",
                "wrong api_key",
                "timeout is too small",
                "timeout is too large"]
            self.assertIn(doc["error"], error_msgs)

        return r

    def test_it_creates_check(self):
        """Verify that create check functionanlity works as expected."""

        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        assert "last_ping" in doc
        self.assertFalse(doc["last_ping"])
        self.assertEqual(doc["n_pings"], 0)

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        """Test creating check with api_key in header instead of request body."""

        payload = {"name": "Foo"}

        r = self.post(payload, None, "abc")
        self.assertEqual(r.status_code, 201)
        self.assertIn(b"Foo", r.content)

    def test_it_handles_missing_request_body(self):
        """Test creating check with missing request body."""

        r = self.post({})

        self.assertEqual(r.status_code, 400)
        self.assertIn(b"wrong api_key", r.content)

    def test_it_handles_invalid_json(self):
        """Test that invalid json in request body appropriately handled."""

        payload = {'api_key': "abc", "name": '%s' % 'foo'.encode("windows-1252")}
        r = self.client.post(self.URL, payload,
                                content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertIn(b"could not parse request body", r.content)

    def test_it_rejects_wrong_api_key(self):
        """Test if wrong api key rejected."""

        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        """Test that non-number timeout value rejected."""

        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        """Test taht non-string name value rejected."""

        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    def test_it_assigns_channels(self):
        """Test for the assignment of channels."""

        ch = Channel(user=self.alice, kind="slack", value="test-token")
        ch.save()

        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60,
            "channels": "*"
        })
        self.assertEqual(r.status_code, 201)

        self.assertTrue(Channel.objects.filter(checks__name="Foo"))

    def test_it_rejects_timeout_too_small(self):
        """Test that timeout values less than allowed minimum(60 secs) rejected."""

        self.post({"api_key": "abc", "name": False, "timeout":10},
                  expected_error="timeout is too small")
    
    def test_it_rejects_timeout_too_large(self):
        """Test that timeout values greater than allowed maximum(604800 secs) rejected."""

        self.post({"api_key": "abc", "name": False, "timeout":100000},
                  expected_error="timeout is too large")

