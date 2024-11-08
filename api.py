import json

import requests
import config

class API:
    def __init__(self):
        pass
    def request_post(self, method, params):
        url = f'{config.url}/{method}'
        response = requests.post(url, params)
        return json.loads(response.text)


#api = API()
#response = api.request_post('auth',{'login': 'fefefe@mail.ru', 'password': '12345'} )
#print(response)
