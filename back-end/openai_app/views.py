from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from openai_app.serialzers import OccupationSerializer, Occupation
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

        ccuser = get_object_or_404(CCUser, id=request.user.id)

        # 1) We need to check the db if it already has occupations for this user

        # 2.a) If we have occupations, return those

        # 2.b) If we do not have occupations, perform the request

        occupations = Occupation.objects.filter(user=ccuser)

        if occupations:
            print(f"We found something")
        else:
            # This is only run if we don't have any results in the db
            #TODO: Add response error handling (errors from OpenAI)
            # Uncomment to allow openai call
            openai_response = openai_get_occupations(env.get('OPENAI_API_KEY'))

            openai_occupations = openai_response['occupations']

            data = [job for job in openai_occupations]

            print(f"Response List: {openai_response['occupations']}")

            # 3) Store the occupations that we get back from openai
            

        response = OccupationSerializer(occupations, many=True).data



        return Response(response)
        # return Response("ok")