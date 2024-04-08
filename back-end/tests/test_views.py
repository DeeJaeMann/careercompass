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

class TestKeywordView(TestCase):
    """
    Keyword View Tests
    """
    tst_email = "me@here.com"
    tst_pass = "1234"

    app_con = "application/json"

    good_usr_data = {
        "email":tst_email,
        "password":tst_pass,
    }

    tst_category = "interest"
    tst_name = "history"

    good_cat_data = {
        "category":tst_category,
        "name":tst_name,
    }

    def test_011_create_keyword_without_credentials(self):
        """
        This test will attempt to create a keyword without credentials
        """
        client = Client()
        response = client.post(
            reverse("create-keyword"),
            data=self.good_cat_data,
            content_type=self.app_con
        )
        self.assertEqual(response.status_code, 401)
    
    def setUp(self):
        """
        Keywords require a user to be authenticated
        """
        client = Client()

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

    def test_012_create_keyword_with_credentials(self):
        """
        This test will attempt to create a keyword with credentials
        """
        response = self.auth_client.post(
            reverse("create-keyword"),
            data=self.good_cat_data,
            content_type=self.app_con,
            )
        
        with self.subTest():
            self.assertEqual(response.status_code, 201)
        self.assertRegex(response.content, rb"history")
        self.assertRegex(response.content, rb"interest")

    def test_013_create_keyword_with_incorrect_category(self):
        """
        This test will attempt to create a keyword with the incorrect category
        """
        response = self.auth_client.post(
            reverse("create-keyword"),
            data={
                "category":"bad",
                "name":self.tst_name
            },
            content_type=self.app_con
        )
        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(response.content, rb"Category")

    def test_014_create_keyword_with_incorrect_name(self):
        """
        This test will attempt to create a keyword with the incorrect name
        """
        response = self.auth_client.post(
            reverse("create-keyword"),
            data={
                "category":self.tst_category,
                "name":"1234"
            },
            content_type=self.app_con
        )
        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(response.content, rb"Name")

    def test_015_create_duplicate_keyword(self):
        """
        This test will attempt to create a duplicate keyword
        """
        self.auth_client.post(
            reverse("create-keyword"),
            data=self.good_cat_data,
            content_type=self.app_con
        )
        response = self.auth_client.post(
            reverse("create-keyword"),
            data=self.good_cat_data,
            content_type=self.app_con
        )
        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(response.content, rb"unique set")