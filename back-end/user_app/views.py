from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from .models import CCUser

# Create your views here.

def create_user(request):
    data = request.data.copy()
    # Model username is email
    data['username'] = request.data.get("email")

    new_user = CCUser(**data)

    try:
        new_user.full_clean()
        new_user = CCUser.objects.create_user(**data)
        token = Token.objects.create(user=new_user)
        return [new_user, token]
    except ValidationError as error:
        return error
    
def SignUp(APIView):
    
    def post(self, request):
        credentials = create_user(request)

        # create_user returns a list if the user data is valid
        if type(credentials) == list:
            new_user, token = credentials
            # Ensure these fields are set to false to prevent accidental admin/superuser creation
            new_user.is_staff = False
            new_user.is_superuser = False
            new_user.save()
            return Response(
                {"user":new_user.username, "token":token.key}, 
                status=HTTP_201_CREATED
                )
        
        return Response(credentials.message_dict, status=HTTP_400_BAD_REQUEST)