from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError
from user_app.models import CCUser

# Part I: User Model
class TestCCUser(TestCase) :
    def test_001_user_with_proper_email_field(self):
        new_ccuser = CCUser.objects.create(
            email="me@here.com",
            username="me@here.com",
            password="1234",
        )

        new_ccuser.full_clean()
        self.assertIsNotNone(new_ccuser)

    def test_002_user_with_improper_email_field(self):
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