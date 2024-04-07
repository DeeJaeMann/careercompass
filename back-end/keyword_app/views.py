import logging
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from user_app.views import TokenReq, CCUser
from .models import Keyword

logger = logging.getLogger("django_info")
logger.setLevel(logging.INFO)

# Create your views here.

class CreateKeyword(TokenReq):
    """
    View to create a new keyword
    """

    def post(self, request):

        data = request.data.copy()
        username = data.get("email")
        this_user = CCUser.objects.get(username=username)

        # print(f"User identified: {this_user.username}")

        return Response("Ok")