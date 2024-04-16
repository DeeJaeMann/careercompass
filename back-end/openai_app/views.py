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
from onet_app.serializers import DetailsSerializer, Details
from user_app.views import TokenReq, CCUser
from keyword_app.serializers import Keyword, KeywordSerializer
from lib.logger import info_logger, error_logger, crit_logger
from lib.openai import openai_get_occupations, openai_verify_key
from lib.onet import OnetWebService
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
                error_logger.error(
                    f"Occupation: User: {ccuser} referenced with no keywords defined")
                return Response("You must have keywords defined", status=HTTP_400_BAD_REQUEST)

            ser_keywords = KeywordSerializer(keywords, many=True)

            # 1) We need to check the db if it already has occupations for this user

            occupations = Occupation.objects.filter(user=ccuser)
            # 2.a) If we have occupations, return those
            if occupations:
                response = OccupationSerializer(occupations, many=True).data
            else:
                # 2.b) If we do not have occupations, perform the request
                # TODO: Add handling for no token provided
                # TODO: Add response handling for not enough tokens (account)
                # TODO: Add response error handling (errors from OpenAI)

                openai_response = openai_get_occupations(
                    openai_key, ser_keywords)

                openai_occupations = openai_response['occupations']

                # 3) Store the occupations that we get back from openai

                job_data = [dict(job, **{'user': ccuser.id})
                            for job in openai_occupations]

                new_occupations = OccupationSerializer(
                    data=list(job_data), many=True)

                if new_occupations.is_valid():
                    new_occupations.save()
                    info_logger.info(
                        f"Occupations: Created for user {ccuser} - Data: {job_data}")

                    onet_user = env.get('ONET_USERNAME')
                    onet_pass = env.get('ONET_PASSWORD')

                    # This is where we need to fire off the request to ONet for the occupation short desc

                    # TODO: Add check to ensure the user and password are not default values and that they exist. If they do not we need to exit with a critical configuration error

                    onet_client = OnetWebService(onet_user, onet_pass)

                    # loop through each job to get the job details from the ONet API
                    for job in job_data:
                        this_occupation = Occupation.objects.get(
                            onet_code=job['onet_code'])

                        # This endpoint provides the occupation overview data
                        # Example: https://services.onetcenter.org/ws/mnm/careers/39-9031.00/
                        this_url = f'mnm/careers/{job["onet_code"]}'
                        this_response = onet_client.call(this_url)

                        # Fomat the response into data for the serializer
                        if 'error' in this_response:
                            # If we get an error in the response, we will add an error entry in the details record. This is also added to the error log
                            error_logger.error(
                                f"OnetWebService: Resource does not exist: {job['onet_code']} - {job['name']}")
                            detail_data = {
                                'onet_name': 'Error',
                                'description': 'This resourse was not found. No additional details are available.',
                                'occupation': this_occupation.id,
                            }
                        else:
                            # Good data found
                            detail_data = {
                                'onet_name': this_response['title'],
                                'description': this_response['what_they_do'],
                                'tasks': this_response['on_the_job'],
                                'alt_names': this_response['also_called'],
                                'occupation': this_occupation.id,
                            }

                        ser_this_job = DetailsSerializer(data=detail_data)

                        if ser_this_job.is_valid():
                            ser_this_job.save()

                            info_logger.info(
                                f"Details: Added {ser_this_job.data}")
                        else:
                            # This should never execute
                            crit_logger.critical(
                                f"DetailsSerializer error: {ser_this_job}")

                    # We only return the occupation data to the requester.  The details will be requested from a different endpoint.
                    # TODO: Determine if this response should include both.  If so, the response for when data already exists in the db needs to be modified as well
                    return Response(new_occupations.data, status=HTTP_201_CREATED)

                # TODO: Verify if this already solves the payment issue.  The error would be in .errors
                # Rate limit and exceeded billing response: 429
                error_logger.error(
                    f"Occupations: Failed to create for User: {ccuser} Data: {job_data} Error: {new_occupations.errors}")
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
