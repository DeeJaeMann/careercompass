import logging
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
    HTTP_400_BAD_REQUEST,
)
from .models import CCUser

logger = logging.getLogger("django_info")
logger.setLevel(logging.INFO)

# Create your views here.

def create_user(request):
    """
    Attempts to create a user model with the data provided
    """
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
    
class TokenReq(APIView):
    """
    Class to inherit when a token is required
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
class SignUp(APIView):
    """
    View to create a new user
    """
    def post(self, request):
        credentials = create_user(request)

        # create_user returns a list if the user data is valid
        if type(credentials) == list:
            new_user, token = credentials
            # Ensure these fields are set to false to prevent accidental admin/superuser creation
            new_user.is_staff = False
            new_user.is_superuser = False
            new_user.save()
            logger.info(f"User: {new_user.username} created.")

            return Response(
                {"username":new_user.username, "token":token.key}, 
                status=HTTP_201_CREATED
                )
        
        return Response(credentials.message_dict, status=HTTP_400_BAD_REQUEST)
    
class LogIn(APIView):
    """
    View to login user
    """

    def post(self, request):

        data = request.data.copy()

        data['username'] = request.data.get("email")

        this_user = authenticate(username=data.get("username"), password=data.get("password"))

        if this_user:

            token, _ = Token.objects.get_or_create(user=this_user)
            login(request, this_user)
            logger.info(f"User: {this_user.username} login.")
            return Response({"username":this_user.username, "token":token.key})
        
        return Response("Username or password incorrect", status=HTTP_400_BAD_REQUEST)

class LogOut(TokenReq):
    """
    View to logout user
    """

    def post(self, request):
        request.user.auth_token.delete()
        logger.info(f"User: {request.data.get('email')} logout.  Token deleted.")
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)