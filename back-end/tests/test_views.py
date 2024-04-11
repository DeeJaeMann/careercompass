from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from keyword_app.models import Keyword, CCUser
from onet_app.models import Details, Occupation
import json
import re

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
        this_auth_client = self.auth_client
        response = this_auth_client.post(
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
        this_auth_client = self.auth_client
        response = this_auth_client.post(
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
        this_auth_client = self.auth_client
        this_auth_client.post(
            reverse("create-keyword"),
            data=self.good_cat_data,
            content_type=self.app_con
        )
        response = this_auth_client.post(
            reverse("create-keyword"),
            data=self.good_cat_data,
            content_type=self.app_con
        )
        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(response.content, rb"unique set")

    def keyword_additional_setup(self):
        """
        This is to create an additional user and two keywords
        One keyword is assigned per user
        """

        self.ccuser_one = CCUser.objects.get(username=self.tst_email)

        self.ccuser_two = CCUser.objects.create(
            email="you@here.com",
            username="you@here.com",
            password="1234",
        )
        self.ccuser_two.full_clean()
        self.ccuser_two.save()

        self.keyword_one = Keyword.objects.create(
            category=self.tst_category,
            name=self.tst_name,
            user=self.ccuser_one,
        )
        self.keyword_one.full_clean()
        self.keyword_one.save()

        self.keyword_two = Keyword.objects.create(
            category=self.tst_category,
            name=self.tst_name,
            user=self.ccuser_two,
        )
        self.keyword_two.full_clean()
        self.keyword_two.save()

    def test_016_user_access_keyword(self):
        """
        This test attempts to access a keyword which belongs to the same user
        """

        self.keyword_additional_setup()

        this_auth_client = self.auth_client
        response = this_auth_client.get(
            reverse("get-keyword", args=[self.keyword_one.id])
        )
        # print(f"response: {response.content}")
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content, rb'"name":"history"')

    def test_017_user_access_other_user_keyword(self):
        """
        This test attemtps to access a keyword that does not belong to the same user
        """

        self.keyword_additional_setup()

        # self.keyword_additional_setup()
        this_auth_client = self.auth_client
        response = this_auth_client.get(
            reverse("get-keyword", args=[self.keyword_two.id])
        )
        # print(f"Response {response.content}")
        # print(f"Keywords {Keyword.objects.order_by('id')}")
        
        with self.subTest():
            self.assertEqual(response.status_code, 403)
        # The keyword needs to be converted to a string and encoded to concat to the binary string RegEx pattern
        id_pattern = re.compile(rb"ID: " + str(self.keyword_two.id).encode())
        self.assertRegex(response.content, id_pattern)

    def test_018_access_keyword_without_credentials(self):
        """
        This test will attempt to access a keyword without credentials
        """

        self.keyword_additional_setup()

        client = Client()
        response = client.get(
            reverse("get-keyword", args=[10])
        )
        self.assertEqual(response.status_code, 401)

    def test_019_access_all_user_keywords(self):
        """
        This test will attempt to access all keywords for the logged in user
        """

        self.keyword_additional_setup()

        new_keyword = Keyword.objects.create(
            category=self.tst_category,
            name="music",
            user=self.ccuser_one
        )

        new_keyword.full_clean()
        new_keyword.save()

        this_auth_client = self.auth_client

        response = this_auth_client.get(reverse("user-keywords"))

        with self.subTest():
            self.assertEqual(response.status_code, 200)
        # Compile the variables specified earlier into a bytes pattern
        key_one_pattern = re.compile(rb'"name":"'+self.tst_name.encode()+b'"')
        key_two_pattern = re.compile(rb'"name":"'+new_keyword.name.encode()+b'"')
        self.assertRegex(response.content, key_one_pattern)
        self.assertRegex(response.content, key_two_pattern)

    def test_020_access_all_user_keywords_no_credentials(self):
        """
        This test will attempt to access the keywords endpoint without credentials
        """
        self.keyword_additional_setup()

        client = Client()
        response = client.get(reverse("user-keywords"))
        self.assertEqual(response.status_code, 401)

class TestOccupationView(TestCase):
    """
    Occupation view tests
    """
    tst_email = "me@here.com"
    tst_pass = "1234"

    app_con = "application/json"

    good_usr_data = {
        "email":tst_email,
        "password":tst_pass,
        }

    def setUp(self):
        """
        Occupations require a user to be authenticated
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

    def setup_keywords(self):
        ccuser = CCUser.objects.get(username=self.tst_email)

        interest_one = Keyword.objects.create(
            category="interest",
            name="music",
            user=ccuser,
        )
        interest_one.full_clean()
        interest_one.save()

        interest_two = Keyword.objects.create(
            category="interest",
            name="history",
            user=ccuser,
        )
        interest_two.full_clean()
        interest_two.save()

        interest_three = Keyword.objects.create(
            category="interest",
            name="logic",
            user=ccuser,
        )
        interest_three.full_clean()
        interest_three.save()

        hobby_one = Keyword.objects.create(
            category="hobby",
            name="swimming",
            user=ccuser,
        )
        hobby_one.full_clean()
        hobby_one.save()

        hobby_two = Keyword.objects.create(
            category="hobby",
            name="woodworking",
            user=ccuser,
        )
        hobby_two.full_clean()
        hobby_two.save()

        hobby_three = Keyword.objects.create(
            category="hobby",
            name="reading",
            user=ccuser,
        )
        hobby_three.full_clean()
        hobby_three.save()

    def test_023_access_occupations(self):
        """
        This test attempts to access all occupations for the authenticated user
        """
        self.setup_keywords()

        this_auth_client = self.auth_client

        response = this_auth_client.get(reverse("get-occupations"))
        self.assertEqual(response.status_code, 201)
    
    def test_024_access_occupations_no_credentials(self):
        """
        This test attempts to access all occupations endpoint without credentials
        """
        self.setup_keywords()

        client = Client()
        response = client.get(reverse("get-occupations"))
        self.assertEqual(response.status_code, 401)

    def test_025_access_stored_occupations(self):
        """
        This test attempts to access occupations stored in the DB.  Occupations are stored on first request, so this makes two requests
        """
        self.setup_keywords()

        this_auth_client = self.auth_client

        this_auth_client.get(reverse("get-occupations"))

        response = this_auth_client.get(reverse("get-occupations"))
        self.assertEqual(response.status_code, 200)

    def test_026_access_occupations_without_keywords(self):
        """
        This test attempts to access occupations without keywords in the DB
        """
        this_auth_client = self.auth_client

        response = this_auth_client.get(reverse("get-occupations"))

        with self.subTest():
            self.assertEqual(response.status_code, 400)
        self.assertRegex(response.content, rb'keywords')

    def test_027_delete_all_user_occupations(self):
        """
        This test attempts to delete all occupations registered to a user
        """
        this_auth_client = self.auth_client

        self.setup_keywords()

        this_auth_client.get(reverse("get-occupations"))

        response = this_auth_client.delete(reverse("get-occupations"))

        occupations = Occupation.objects.all()

        with self.subTest():
            self.assertEqual(response.status_code, 204)
        self.assertEqual(len(occupations), 0)

    def test_029_occupation_populates_details(self):
        """
        This test verifies that when occupations are created, details entries are created as well
        """
        this_auth_client = self.auth_client

        self.setup_keywords()

        this_auth_client.get(reverse("get-occupations"))

        details = Details.objects.all()

        self.assertNotEqual(len(details), 0)