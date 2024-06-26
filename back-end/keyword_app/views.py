from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from user_app.views import TokenReq, CCUser
from openai_app.models import Occupation
from .serializers import KeywordSerializer, Keyword
from lib.logger import info_logger, error_logger, warn_logger

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
            info_logger.info(
                f"Keyword ID: {new_keyword.data.get('id')} created by User: {this_user.get_username()}")
            return Response(new_keyword.data, status=HTTP_201_CREATED)

        error_logger.error(
            f"CreateKeyword: {new_keyword.errors} Value: {data}")
        return Response(new_keyword.errors, status=HTTP_400_BAD_REQUEST)


class KeywordInfo(TokenReq):
    """
    View to get keyword field data
    """

    #TODO: Is this one actually needed?

    def get(self, request, id):

        this_user = get_object_or_404(CCUser, id=request.user.id)
        this_keyword = get_object_or_404(Keyword, id=id)

        if this_keyword.user == this_user:

            ser_keyword = KeywordSerializer(this_keyword)
            info_logger.info(
                f"Keyword accessed: ID: {ser_keyword.data['id']} Name: {ser_keyword.data['name']}"
            )

            return Response(ser_keyword.data)

        warn_logger.warning(
            f"Keyword access failed: User: {this_user} attempted to access Keyword ID: {this_keyword.id} Name: {this_keyword.name}")
        return Response(f"Keyword ID: {this_keyword.id} Name: {this_keyword.name} does not belong to user {this_user}", status=HTTP_403_FORBIDDEN)
    
    def put(self, request, id):
        ccuser = get_object_or_404(CCUser, id=request.user.id)
        keyword = get_object_or_404(Keyword, id=id)
        
        data = request.data.copy()

        update_keyword = KeywordSerializer(keyword, data=data, partial=True)

        # Update data_added
        update_keyword.initial_data['date_added'] = timezone.now()

        if update_keyword.is_valid():
            update_keyword.save()
            info_logger.info(f"Keyword: User: {ccuser} updated ID: {id} - {update_keyword.data}")
            # This will have to delete the listed occupations
            old_occupations = Occupation.objects.filter(user=ccuser.id)
            print(f"Occupations: ")
            info_logger.info(f"Keyword: Delete old occupations for {ccuser} - {[(job.id, job.name) for job in old_occupations]}")
            old_occupations.delete()
            return Response(update_keyword.data, status=HTTP_201_CREATED)
        error_logger.error(f"Keyword: User {ccuser} failed to update {id} - {update_keyword.errors}")
        return Response(update_keyword.errors, status=HTTP_400_BAD_REQUEST)


class KeywordAllInfo(TokenReq):
    """
    View to get all user's keywords
    """

    def get(self, request):
        this_user = get_object_or_404(CCUser, id=request.user.id)
        keywords = Keyword.objects.filter(user=this_user)
        ser_keywords = KeywordSerializer(keywords, many=True)
        info_logger.info(
            f"Keywords accessed (All User: {this_user}): {ser_keywords.data}")
        return Response(ser_keywords.data)

