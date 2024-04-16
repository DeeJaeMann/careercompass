from openai import OpenAI, AuthenticationError
import json


def openai_verify_key(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
    except AuthenticationError:
        return False
    return True


def openai_get_occupations(api_key, ser_keywords):

    # Create the OpenAI client with the api key
    client = OpenAI(api_key=api_key)

    # TODO: Make this more dynamic later
    interests = [key['name']
                 for key in ser_keywords.data if key['category'] == 'interest']
    hobbies = [key['name']
               for key in ser_keywords.data if key['category'] == 'hobby']

    # Client configuration
    prompt = f"given these 3 interests: {interests[0]}, {interests[1]}, {interests[2]} and these 3 hobbies: {hobbies[0]}, {hobbies[1]}, {hobbies[2]}.  generate 5 ocupations with the ONet job code that would match them.  the result should be in json format.  the occupation name should be name and the job code should be onet_code"
    model = "gpt-3.5-turbo"

    # Make the request
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        response_format={
            'type': 'json_object'
        }
    )

    # Convert the response message into json
    json_response = json.loads(response.choices[0].message.content)

    return json_response
