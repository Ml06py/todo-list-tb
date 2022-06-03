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

    def Register(self, first_name, last_name, userid, password):
        '''
            Register user to website
        '''
        # json to send
        base_json = {"first_name": first_name,"last_name": last_name,"telegram_id": userid,"token": "","password": password}
        # request
        request = requests.post(f"{self.url}/tb-register/", json=base_json, headers={'content-type': 'application/json'}).content.decode("UTF-8")
        return_val = json.loads(request)

        if "token" and "username" in return_val:
            return True,  return_val["token"], return_val["username"]
        else:
            return False