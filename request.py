import requests, json


class Request():
    def __init__(self):
        # The main url
        self.url = "http://127.0.0.1:8000/api/v1"

    def Login(self, username, token, userid):
        '''
            Send login request to website
        '''
        request = requests.get(f"{self.url}/tb-login/{username}/{token}/{userid}/").content.decode("utf-8") 
        response = json.loads(request)
        if "found" in response:
            return True
        else:
            return False
        
