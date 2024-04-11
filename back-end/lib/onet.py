from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from base64 import standard_b64encode
import json


class OnetWebService:
    """
    This class is modified from the ONet example at:  https://github.com/onetcenter/web-services-samples/blob/master/python-3/OnetWebService.py
    """

    def __init__(self, username, password):
        encode_message = f'{username}:{password}'
        self._headers = {
            'User-Agent': 'python-OnetWebService-modified/1.00 (bot)',
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
            handle = urlopen(request)
        except HTTPError as error:
            # Invalid data sent to API
            if error.code == 422:
                return json.load(error)

            return {'error': f'Call to {url} failed with error code {str(error.code)}'}
        except URLError as error:
            return {'error': f'Call to {url} failed with reason: {str(error.reason)}'}
        code = handle.getcode()

        if code not in [200, 422]:
            return {
                'error': f'Call to {url} failed with error code {str(code)}',
                'urllib2_info': handle}
        return json.load(handle)
