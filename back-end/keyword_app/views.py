from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from user_app.views import TokenReq, CCUser
from .serializers import KeywordSerializer, Keyword
from lib.logger import info_logger, error_logger

# Create your views here.

class CreateKeyword(TokenReq):
    """
    View to create a new keyword
    """

    def post(self, request):

        data = request.data.copy()
        this_user = get_object_or_404(CCUser, id=request.user.id)
        data['user'] = this_user.id

        new_keyword = KeywordSerializer(data=data)

        if new_keyword.is_valid():
            new_keyword.save()
            info_logger.info(f"Keyword ID: {new_keyword.data.get('id')} created by User: {this_user.get_username()}")
            return Response(new_keyword.data, status=HTTP_201_CREATED)
        
        error_logger.error(f"CreateKeyword: {new_keyword.errors} Value: {data}")
        return Response(new_keyword.errors, status=HTTP_400_BAD_REQUEST)