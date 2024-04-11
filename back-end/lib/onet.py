from urllib.request import Request
from urllib.error import HTTPError, URLError
from base64 import standard_b64encode
import json


class OnetWebService:

    def __init__(self, username, password):
        encode_message = f'{username}:{password}'
        self._headers = {
            'User-Agent': 'python-OnetWebService/1.00 (bot)',
            'Authorization': 'Basic ' +    
            standard_b64encode((encode_message).encode()).decode,
            'Accept': 'application/json',
        }
        self._url_root = 'https://services.onetcenter.org/ws/'

    def call(self, path, *query):
        url = self._url_root + path

        request = Request(url, None, self._headers)
        handle = None

        try:
            handle = Request.urlopen(request)
        except HTTPError as error:
            if error.code == 422:
                #Invalid data
                return json.load(error)
            return {'error': f'Call to {url} failed with error code {str(error.code)}'}
        except URLError as error:
            return {'error': f'Call to {url} failed with reason: {str(error.reason)}'}
        code = handle.getcode()