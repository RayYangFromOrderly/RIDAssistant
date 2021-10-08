import os
import urllib
from .settings import Settings

def touch_api(url, data = None, method='post'):
    url = '/'.join([Settings.server_url, 'api', url])
    if method == 'post':
        response = requests.post(url, params=data)
    import pdb;pdb.set_trace()
    if response.status_code != 200:
        return False
    return response.json()
