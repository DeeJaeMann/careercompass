from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
import json

class TestCCUserView(TestCase):
    """
    CCUser View Tests
    """

    tst_email = "me@here.com"
    tst_pass = "1234"

    app_con = "application/json"

    good_usr_data = {
        "email":tst_email,
        "password":tst_pass,
    }
    
    def test_003_user_sign_up(self):
        """
        This test will attempt to create a new user given the correct information
        """

        client = Client()
        response = client.post(
            reverse("sign-up"),
            data=self.good_usr_data,
            content_type=self.app_con,
        )
        with self.subTest():
            self.assertEqual(response.status_code, 201)

        self.assertRegex(response.data['username'], self.tst_email)
    
    def test_004_user_sign_up_improper_email(self):
        """
        This test will attempt to create a new user given an incorrect email address
        """
        client = Client()
        response = client.post(
            reverse("sign-up"),
            data={
                "email":"me", 
                "password":self.tst_pass
                },
            content_type=self.app_con,
        )
        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(response.content, rb"valid email")

    def test_005_user_login(self):
        """
        This test will sign up a new user and attempt to login given the correct credentials
        """

        client = Client()
        # Sign up for account
        client.post(
            reverse("sign-up"),
            data=self.good_usr_data,
            content_type=self.app_con,
        )
        response = client.post(
            reverse("login"),
            data=self.good_usr_data,
            content_type=self.app_con,
        )

        with self.subTest():
            self.assertEqual(response.status_code, 200)
        self.assertRegex(
            response.data['username'], self.tst_email
        )

    def test_006_user_login_incorrect_password(self):
        """
        This test will sign up a new user and attemt to login given the incorrect credentials
        """

        client = Client()
        # Sign up for account
        client.post(
            reverse("sign-up"),
            data=self.good_usr_data,
            content_type=self.app_con,
        )
        response = client.post(
            reverse("login"),
            data={
                "email":self.tst_email, 
                "password":"incorrect",
                },
            content_type=self.app_con,
        )

        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(
            response.content, rb"(?:U|username)+.*(?:P|password)+.*(?:I|incorrect)+"
        )

    def test_007_user_logout(self):
        """
        This test will sign up a new user, log them in and attempt to log them out with credentials provided
        """
        client = Client()

        # Sign up for account
        client.post(
            reverse("sign-up"),
            data=self.good_usr_data,
            content_type=self.app_con,
        )
        login_response = client.post(
            reverse("login"),
            data=self.good_usr_data,
            content_type=self.app_con,
        )
        response_body = json.loads(login_response.content)
        self.auth_client = Client(headers={"Authorization":f"Token {response_body['token']}"})
        response = self.auth_client.post(reverse("logout"))
        with self.subTest():
            tokens = Token.objects.all()
            self.assertEqual(len(tokens), 0)
        self.assertEqual(response.status_code, 204)