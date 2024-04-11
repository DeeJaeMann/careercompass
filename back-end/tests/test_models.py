from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError
from keyword_app.models import Keyword, CCUser
from onet_app.models import Occupation, Details, Knowledge, Education


class TestCCUser(TestCase):
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


class TestOccupation(TestCase):
    """
    Occupation Model Tests
    """

    def setUp(self):
        """
        Occupation require a user to be created
        """
        CCUser.objects.create(
            email="me@here.com",
            username="me@here.com",
            password="1234",
        )

    def test_021_occupation_with_proper_fields(self):
        """
        This test will attempt to create an occupation with the correct fields
        """
        ccuser = CCUser.objects.get(username="me@here.com")

        new_occupation = Occupation.objects.create(
            name="Musician or Singer",
            onet_code="27-2042.02",
            user=ccuser,
        )

        new_occupation.full_clean()
        self.assertIsNotNone(new_occupation)

    def test_022_occupation_with_incorrect_onet_code(self):
        """
        This test will attempt to create an occupation with the incorrect onet_code
        """
        ccuser = CCUser.objects.get(username="me@here.com")

        try:
            new_occupation = Occupation.objects.create(
                name="Musician or Singer",
                onet_code="bad code",
                user=ccuser,
            )

            new_occupation.full_clean()
            self.fail()
        except ValidationError as error:
            self.assertTrue("onet_code" in error.message_dict)


class TestOnetModels(TestCase):
    """
    ONet Model Tests
    """

    def setUp(self):
        """
        Occupation require a user to be created
        """
        ccuser = CCUser.objects.create(
            email="me@here.com",
            username="me@here.com",
            password="1234",
        )
        """
        Details require an occupation to be created
        """
        self.job = Occupation.objects.create(
            name="Swim Coach",
            onet_code="27-2022.00",
            user=ccuser,
        )
        self.onet_name = "Coaches & Scouts"
        self.description = "Instruct or coach groups or individuals in the fundamentals of sports for the primary purpose of competition. Demonstrate techniques and methods of participation. May evaluate athletes' strengths and weaknesses as possible recruits or to improve the athletes' technique to prepare them for competition. Those required to hold teaching certifications should be reported in the appropriate teaching category."
        self.tasks = {
            "task": [
                "Plan, organize, and conduct practice sessions.",
                "Provide training direction, encouragement, motivation, and nutritional advice to prepare athletes for games, competitive events, or tours.",
                "Adjust coaching techniques, based on the strengths and weaknesses of athletes."
            ]
        }
        self.alt_names = {
            "title": [
                "Basketball Coach",
                "Coach",
                "Football Coach",
                "Track and Field Coach"
            ]
        }

    def test_028_details_with_proper_fields(self):
        """
        This test will attempt to create a new details model
        """
        
        new_details = Details.objects.create(
            onet_name=self.onet_name,
            description=self.description,
            tasks=self.tasks,
            alt_names=self.alt_names,
            occupation=self.job,
        )

        new_details.full_clean()
        self.assertIsNotNone(new_details)

    def test_031_knowledge_with_proper_fields(self):
        """
        This test will attempt to create a new knowledge model
        """

        new_knowledge = Knowledge.objects.create(
            category="Test category",
            description="This is a test",
            occupation=self.job,
        )

        new_knowledge.full_clean()
        self.assertIsNotNone(new_knowledge)

    def test_032_eductation_with_proper_fields(self):
        """
        This test will attempt to create a new education model
        """

        new_education = Education.objects.create(
            category="certificate after high school",
            occupation=self.job,
        )

        new_education.full_clean()
        self.assertIsNotNone(new_education)