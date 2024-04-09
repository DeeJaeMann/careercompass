from openai import OpenAI
import json

def openai_get_occupations(api_key):

    # Create the OpenAI client with the api key
    client = OpenAI(api_key=api_key)

    # Client configuration
    prompt = "given these 3 interests: music, history, logic and these 3 hobbies: swimming, woodworking, reading.  generate 5 ocupations with the ONet job code that would match them.  the result should be in json format"
    model="gpt-3.5-turbo"

    # Make the request
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

    # Convert the response message into json
    json_response = json.loads(response.choices[0].message.content)

    return json_response