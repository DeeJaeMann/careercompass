from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from user_app.views import TokenReq, CCUser
from openai_app.models import Occupation
from .serializers import DetailsSerializer, Details, KnowledgeSerializer, Knowledge
from lib.logger import info_logger, error_logger
from lib.onet import OnetWebService
from careercompass_api.settings import env

# Create your views here.

onet_user = env.get('ONET_USERNAME')
onet_pass = env.get('ONET_PASSWORD')

onet_client = OnetWebService(onet_user, onet_pass)

class DetailsInfo(TokenReq):
    """
    View to get details data
    """

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
    """
    View to get knowledge data
    """

    def get(self, request, id):
        """
        This will get the knowledge record(s) for the occupation id provided
        If the no records are in the DB it will request the data from
        the ONet API
        """
        ccuser = get_object_or_404(CCUser, id=request.user.id)

        knowledge = Knowledge.objects.filter(occupation=id)

        if knowledge.count() == 0:
            # No record exists, query ONet API
            print("No Record")
            # occupation = Occupation.objects.get(id=id)
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

            new_knowledge = KnowledgeSerializer(data=knowledge_data, many=True)

            if new_knowledge.is_valid():
                print(f"Serializer is valid {new_knowledge.data}")
                new_knowledge.save()
                info_logger.info(f"Knowledge: User {ccuser} created for occupation ID: {occupation.id} - {new_knowledge.data}")
                return Response(new_knowledge.data, status=HTTP_201_CREATED)
            return Response(new_knowledge.errors, status=HTTP_400_BAD_REQUEST)

        print("Found records")
        response = KnowledgeSerializer(knowledge, many=True)

        return Response(response.data)
    
    def delete(self, request, id):
        """
        Deletes all knowledge records with job id
        """
        this_user = get_object_or_404(CCUser, id=request.user.id)

        Knowledge.objects.filter(occupation=id).delete()
        info_logger.info(f"Knowledge: User: {this_user} deleted knowledge for occupation id: {id}")
        return Response(status=HTTP_204_NO_CONTENT)