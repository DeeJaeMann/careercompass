from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from openai_app.models import Occupation
from user_app.views import TokenReq, CCUser
from lib.logger import info_logger
from lib.occupation import openai_get_occupations
from careercompass_api.settings import env

# Create your views here.
class OpenAIOccupation(TokenReq):
    """
    View to view occupation list
    """

    def get(self, request):

        # This is only run if we don't have any results in the db
        response = openai_get_occupations(env.get('OPENAI_API_KEY'))

        return Response(response)