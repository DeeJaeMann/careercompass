from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from openai_app.serialzers import OccupationSerializer, Occupation
from user_app.views import TokenReq, CCUser
from lib.logger import info_logger, error_logger, crit_logger
from lib.occupation import openai_get_occupations, openai_verify_key
from careercompass_api.settings import env

# Create your views here.
class OpenAIOccupation(TokenReq):
    """
    View to view occupation list
    """

    def get(self, request):

        openai_key = env.get('OPENAI_API_KEY')

        # Verify the key is not blank and that it is valid
        if openai_key and openai_verify_key(openai_key):

            ccuser = get_object_or_404(CCUser, id=request.user.id)

            # 1) We need to check the db if it already has occupations for this user

            occupations = Occupation.objects.filter(user=ccuser)
            # 2.a) If we have occupations, return those
            if occupations:
                response = OccupationSerializer(occupations, many=True).data
            else:
                # 2.b) If we do not have occupations, perform the request
                #TODO: Add handling for no token provided
                #TODO: Add response handling for not enough tokens (account)
                #TODO: Add response error handling (errors from OpenAI)

                openai_response = openai_get_occupations(openai_key)

                openai_occupations = openai_response['occupations']

                # 3) Store the occupations that we get back from openai

                data = [dict(job, **{'user':ccuser.id}) for job in openai_occupations]

                new_occupations = OccupationSerializer(data=list(data), many=True)

                if new_occupations.is_valid():
                    new_occupations.save()
                    info_logger.info(f"Occupations: Created for user {ccuser} - Data: {data}")
                    return Response(response, status=HTTP_201_CREATED)
                
                #TODO: Verify if this already solves the payment issue.  The error would be in .errors
                # Rate limit and exceeded billing response: 429
                error_logger.error(f"Occupations: Failed to create for User: {ccuser} Data: {data} Error: {new_occupations.errors}")
                return Response(f"Error: OpenAI: {new_occupations.errors}", status=HTTP_503_SERVICE_UNAVAILABLE)
            
            return Response(response)
        else:
            crit_logger.critical(f"Configuration: Invalid OpenAI Key provided")
            return Response("Configuration: Invalid OpenAI Key provided", status=HTTP_500_INTERNAL_SERVER_ERROR)