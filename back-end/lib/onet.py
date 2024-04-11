from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from base64 import standard_b64encode
import json


class OnetWebService:
    """
    This class is modified from the ONet example at:  https://github.com/onetcenter/web-services-samples/blob/master/python-3/OnetWebService.py
    """

    def __init__(self, username, password):
        # ONet API Username and Password
        encode_message = f'{username}:{password}'
        # These are the specified headers to connect with the ONet API
        self._headers = {
            'User-Agent': 'python-OnetWebService-modified/1.00 (bot)',
            'Authorization': f'Basic {standard_b64encode((encode_message).encode()).decode()}',
            'Accept': 'application/json',
        }
        self._url_root = 'https://services.onetcenter.org/ws/'

    def call(self, path):
        url = self._url_root + path

        request = Request(url, None, self._headers)
        handle = None

        try:
            handle = urlopen(request)
        except HTTPError as error:
            # Invalid data sent to API
            #TODO: Handle this in the event this error will pop up. The error needs to be recorded in critical issues because all requests are sent via function calls. Users should have no ability to change requests
            if error.code == 422:
                return json.load(error)

            #TODO: Same as above
            return {'error': f'Call to {url} failed with error code {str(error.code)}'}
        except URLError as error:
            #TODO: Same as above
            return {'error': f'Call to {url} failed with reason: {str(error.reason)}'}
        
        code = handle.getcode()

        if code not in [200, 422]:
            return {
                # 404 errors are handled
                #TODO: Others must be handled as well
                'error': f'Call to {url} failed with error code {str(code)}',
                'urllib2_info': handle}
        return json.load(handle)
