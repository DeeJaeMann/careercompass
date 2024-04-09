from openai import OpenAI
import json

def openai_get_occupations(api_key):
    # api_key = env.get('OPENAI_API_KEY')
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

    print(f"Response: {response.choices[0].message.content}")

    json_response = json.loads(response.choices[0].message.content)

    # return response.choices[0].message.content
    return json_response