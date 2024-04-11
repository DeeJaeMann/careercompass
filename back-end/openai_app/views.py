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
from keyword_app.serializers import Keyword, KeywordSerializer
from lib.logger import info_logger, error_logger, crit_logger
from lib.openai import openai_get_occupations, openai_verify_key
from careercompass_api.settings import env

# Create your views here.
class OpenAIOccupation(TokenReq):
    """
    View for occupation list
    """

    def get(self, request):

        openai_key = env.get('OPENAI_API_KEY')

        # Verify the key is not blank and that it is valid
        if openai_key and openai_verify_key(openai_key):
            ccuser = get_object_or_404(CCUser, id=request.user.id)

            # Get the keywords
            keywords = Keyword.objects.filter(user=ccuser)

            # Ensure we have keywords in the DB
            if len(keywords) == 0:
                error_logger.error(f"Occupation: User: {ccuser} referenced with no keywords defined")
                return Response("You must have keywords defined", status= HTTP_400_BAD_REQUEST)

            ser_keywords = KeywordSerializer(keywords, many=True)

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

                openai_response = openai_get_occupations(openai_key, ser_keywords)

                openai_occupations = openai_response['occupations']

                # 3) Store the occupations that we get back from openai

                job_data = [dict(job, **{'user':ccuser.id}) for job in openai_occupations]

                new_occupations = OccupationSerializer(data=list(job_data), many=True)

                if new_occupations.is_valid():
                    new_occupations.save()
                    info_logger.info(f"Occupations: Created for user {ccuser} - Data: {job_data}")
                    # This is where we need to fire off the request to ONet for the occupation short desc
                    # Once the response is received it should create a new entry in the DB - Details table
                    return Response(new_occupations.data, status=HTTP_201_CREATED)
                
                #TODO: Verify if this already solves the payment issue.  The error would be in .errors
                # Rate limit and exceeded billing response: 429
                error_logger.error(f"Occupations: Failed to create for User: {ccuser} Data: {job_data} Error: {new_occupations.errors}")
                return Response(f"Error: OpenAI: {new_occupations.errors}", status=HTTP_503_SERVICE_UNAVAILABLE)
            
            return Response(response)
        else:
            # Invalid OpenAI API Key is a critical error. The rest of the app won't function without it
            crit_logger.critical(f"Configuration: Invalid OpenAI Key provided")
            return Response("Configuration: Invalid OpenAI Key provided", status=HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        """
        Deletes all occupations associated with the user
        """
        ccuser = get_object_or_404(CCUser, id=request.user.id)

        Occupation.objects.filter(user=ccuser).delete()
        info_logger.info(f"Occupation: User: {ccuser} deleted occupations")
        return Response(status=HTTP_204_NO_CONTENT)