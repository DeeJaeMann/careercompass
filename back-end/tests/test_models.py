from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError
from user_app.models import CCUser
from keyword_app.models import Keyword


# Part I: User Model
class TestCCUser(TestCase) :
    """
    CCUser Model Tests
    """
    def test_001_user_with_proper_email_field(self):
        """
        This test will create a user with proper fields
        """
        new_ccuser = CCUser.objects.create(
            email="me@here.com",
            username="me@here.com",
            password="1234",
        )

        new_ccuser.full_clean()
        self.assertIsNotNone(new_ccuser)

    def test_002_user_with_improper_email_field(self):
        """
        This test will attempt to create a user with improper email field
        """
        try:
            new_ccuser = CCUser.objects.create(
                email="me",
                username="me",
                password="1234",
            )

            new_ccuser.full_clean()
            self.fail()
        except ValidationError as error:
            self.assertTrue("email" in error.message_dict)

class TestKeyword(TestCase):
    """
    Keyword Model Tests
    """
    def setUp(self):
        """
        Keywords require a user to be created
        """
        CCUser.objects.create(
            email="me@here.com",
            username="me@here.com",
            password="1234",
        )

    def test_008_keyword_with_proper_fields(self):
        """
        This test will create a new keyword with correct values
        """
        ccuser = CCUser.objects.get(username="me@here.com")

        new_keyword = Keyword.objects.create(
            category="interest",
            name="history",
            user=ccuser,
        )

        new_keyword.full_clean()
        self.assertIsNotNone(new_keyword)

    def test_009_keyword_with_improper_category(self):
        """
        This test will attempt to create a new keyword with the incorrect category
        """
        ccuser = CCUser.objects.get(username="me@here.com")

        try:
            new_keyword = Keyword.objects.create(
                category="bad",
                name="history",
                user=ccuser,
            )

            new_keyword.full_clean()
            self.fail()
        except ValidationError as error:
            self.assertTrue("category" in error.message_dict)

    def test_010_keyword_with_improper_name(self):
        """
        This test will attempt to create a new keyword with the incorrect name format
        """
        ccuser = CCUser.objects.get(username="me@here.com")

        try:
            new_keyword = Keyword.objects.create(
                category="interest",
                name="1234",
                user=ccuser,
            )

            new_keyword.full_clean()
            self.fail()
        except ValidationError as error:
            self.assertTrue("name" in error.message_dict)