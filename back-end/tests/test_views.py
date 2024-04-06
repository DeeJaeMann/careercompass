from django.test import TestCase, Client
from django.urls import reverse

class TestCCUserView(TestCase):
    
    def test_003_user_sign_up(self):
        client = Client()
        response = client.post(
            reverse("sign-up"),
            data={"email":"me@here.com", "password":"1234"},
            content_type="application/json",
        )
        with self.subTest():
            self.assertEqual(response.status_code, 201)
        self.assertTrue(
            b'{"username":"me@here.com"' in response.content
            and b"token" in response.content
        )
    
    def test_004_user_sign_up_improper_email(self):
        client = Client()
        response = client.post(
            reverse("sign-up"),
            data={"email":"me", "password":"1234"},
            content_type="application/json",
        )
        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertTrue(
            b"valid email address" in response.content
        )