from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from user_app.views import TokenReq, CCUser
from openai_app.models import Occupation
from .serializers import DetailsSerializer, Details
from lib.logger import info_logger

# Create your views here.
class DetailsInfo(TokenReq):
    """
    View to get details data
    """

    def get(self, request, id):
        """
        This will get the details for the occupation id provided
        """
        this_user = get_object_or_404(CCUser, id=request.user.id)

        this_details = get_object_or_404(Details, occupation=id)

        ser_details = DetailsSerializer(this_details)

        info_logger.info(f"Details: User {this_user} accessed Detail ID: {this_details.id} - Occupation ID: {id} - {this_details.onet_name}")

        return Response(ser_details.data)