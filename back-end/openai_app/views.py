from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
import requests
import json
from openai import OpenAI
from pprint import PrettyPrinter
from openai_app.models import Occupation
from user_app.views import TokenReq, CCUser
from lib.logger import info_logger
from careercompass_api.settings import env

# Create your views here.
class OpenAIOccupation(TokenReq):
    """
    View to view occupation list
    """
    def openai_get_occupations(self):
        api_key = env.get('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)
        # client.api_key = api_key
        # endpoint = "https://api.openai.com/v1/chat/completions"
        prompt = "given these 3 interests: music, history, logic and these 3 hobbies: swimming, woodworking, reading.  generate 5 ocupations with the ONet job code that would match them.  the result should be in json format"
        model="gpt-3.5-turbo"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role':'user',
                    'content':prompt
                }
            ],
            response_format={
                'type':'json_object'
            }
        )
        # headers = {
        #     'Authorization':f'Bearer {api_key}',
        #     'Content-Type':"application/json"
        # }
        # data = {
        #     'model':model,
        #     'message':[
        #         {
        #             'role':'system',
        #             'content':'You are a helpful assistant.'
        #         },
        #         {
        #             'role':'user',
        #             'content':prompt
        #         },
        #     ],
        #     'temperature': 0.7,
        #     'response_format':{
        #         'type':'json_object'
        #     }
        # }
        # pp = PrettyPrinter(indent=2, depth=2)

        # # print(json.dumps(data))
        # # print(data)

        # response = requests.post(endpoint, json=data, headers=headers)
        print(f"Response: {response.choices[0].message.content}")

        return response
    def get(self, request):
        response = self.openai_get_occupations()

        return Response("OK")