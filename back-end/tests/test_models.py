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
        CCUser.objects.create(
            email="me@here.com",
            username="me@here.com",
            password="1234",
        )

    def test_008_keyword_with_proper_fields(self):
        ccuser = CCUser.objects.get(username="me@here.com")

        new_keyword = Keyword.objects.create(
            category="interest",
            name="history",
            user=ccuser
        )

        new_keyword.full_clean()
        self.assertIsNotNone(new_keyword)