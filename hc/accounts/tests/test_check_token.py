from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_login_redirect(self):
        """Test that it redirects a user once they are logged in"""
        form = {'email': self.alice.email, 'password': 'password'}
        redirect = self.client.post("/accounts/login/", form)
        self.assertRedirects(redirect, "/checks/")

    def test_it_denies_bad_token(self):
        """Test the method that detects a bad token redirects to the login page"""
        token_check = self.client.post("/accounts/check_token/alice/bad_token/")
        self.assertRedirects(token_check, "/accounts/login/")

    ### Any other tests?
