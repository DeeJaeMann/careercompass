from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from user_app.views import TokenReq, CCUser
from openai_app.models import Occupation
from .serializers import (
    DetailsSerializer, 
    Details, 
    KnowledgeSerializer, 
    Knowledge,
    EducationSerializer,
    Education
)
from lib.logger import info_logger, error_logger
from lib.onet import OnetWebService
from careercompass_api.settings import env

# Create your views here.

onet_user = env.get('ONET_USERNAME')
onet_pass = env.get('ONET_PASSWORD')

onet_client = OnetWebService(onet_user, onet_pass)

class DetailsInfo(TokenReq):

    def get(self, request, id):
        """
        This will get the details for the occupation id provided
        """
        ccuser = get_object_or_404(CCUser, id=request.user.id)
        details = get_object_or_404(Details, occupation=id)

        ser_details = DetailsSerializer(details)

        info_logger.info(
            f"Details: User {ccuser} accessed Detail ID: {details.id} - Occupation ID: {id} - {details.onet_name}")

        return Response(ser_details.data)

class KnowledgeInfo(TokenReq):

    def get(self, request, id):
        """
        This will get the knowledge record(s) for the occupation id provided
        If the no records are in the DB it will request the data from
        the ONet API
        """
        ccuser = get_object_or_404(CCUser, id=request.user.id)

        knowledge = Knowledge.objects.filter(occupation=id)

        # Check if we have any records that match the occupation id,
        # If not, we will make the API request to get records
        if knowledge.count() == 0:
            # No record exists, query ONet API
            occupation = get_object_or_404(Occupation, id=id)
            # onet_code
            this_url = f'mnm/careers/{occupation.onet_code}/knowledge'

            response = onet_client.call(this_url)

            knowledge_data = []

            if 'error' in response:
                # If we get an error in the response, we will add an error entry in the knowledge record.  This is also added to the error log
                error_logger.error(
                    f"OnetWebService: Resource does not exist: {occupation.onet_code} - {occupation.name}")

                this_data = {
                    'category': 'Error',
                    'description': {
                        'element': [
                            {
                                'id': 'error',
                                'name': 'this record does not exist'
                            }
                        ]
                    },
                    'occupation': occupation.id,
                }
                knowledge_data.append(this_data)

            else:
                # Good data found

                group = response['group']

                # There may be multiple entries in each group so iterate through the list to create a record for each one
                for element in group:

                    category = element['title']['name']
                    description = {'element':element['element']}
                    this_data = {
                        'category':category,
                        'description':description,
                        'occupation':occupation.id
                    }
                    knowledge_data.append(this_data)

            ser_new_knowledge = KnowledgeSerializer(data=knowledge_data, many=True)

            if ser_new_knowledge.is_valid():
                ser_new_knowledge.save()
                info_logger.info(f"Knowledge: User {ccuser} created for occupation ID: {occupation.id} - {ser_new_knowledge.data}")
                return Response(ser_new_knowledge.data, status=HTTP_201_CREATED)
            return Response(ser_new_knowledge.errors, status=HTTP_400_BAD_REQUEST)

        response = KnowledgeSerializer(knowledge, many=True)

        return Response(response.data)
    
    def delete(self, request, id):
        """
        Deletes all knowledge records with job id
        """
        ccuser = get_object_or_404(CCUser, id=request.user.id)

        Knowledge.objects.filter(occupation=id).delete()
        info_logger.info(f"Knowledge: User: {ccuser} deleted knowledge for occupation id: {id}")
        return Response(status=HTTP_204_NO_CONTENT)
    
class EducationInfo(TokenReq):

    def get(self, request, id):
        ccuser = get_object_or_404(CCUser, id=request.user.id)

        education = Education.objects.filter(occupation=id)

        print(f"\n*****\nGot education: {education}\n*****\n")

        if education.count() == 0:
            occupation = get_object_or_404(Occupation, id=id)

            this_url = f'mnm/careers/{occupation.onet_code}/education'

            response = onet_client.call(this_url)

            description = {}

            # The API will usually return either of the following keys in the response JSON
            if 'apprenticeships' in response:
                description['apprencticeships'] = response['apprenticeships']

            if 'education_usually_needed' in response:
                description['education_usually_needed'] = response['education_usually_needed']

            if 'error' in response:
                description['error'] = "This resource does not exist"
                error_logger.error(f"OnetWebService: Resource does not exist: {occupation.onet_code} - {occupation.name}")

            new_education = {
                'occupation':occupation.id,
                'description':description
            }

            ser_new_education = EducationSerializer(data=new_education)

            if ser_new_education.is_valid():
                ser_new_education.save()
                info_logger.info(f"Education: User {ccuser} created for occupation ID: {occupation.id} - {ser_new_education.data}")
                return Response(ser_new_education.data, status=HTTP_201_CREATED)

            return Response(ser_new_education.errors, status=HTTP_400_BAD_REQUEST)
        
        # Count was used to determine if records exist, if they do, there
        # will only be one, so reference the first of the query set
        response = EducationSerializer(education.first())

        return Response(response.data)
    
    def delete(self, request, id):
        """
        Deletes education record with job id
        """
        ccuser = get_object_or_404(CCUser, id=request.user.id)

        Education.objects.get(occupation=id).delete()
        info_logger.info(f"Education: User: {ccuser} deleted education for occupation id: {id}")
        return Response(status=HTTP_204_NO_CONTENT)