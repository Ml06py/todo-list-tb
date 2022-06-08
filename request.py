import requests, json
from io import BytesIO


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
        request = requests.post(f"{self.url}/tb-register/", json=base_json,
                                 headers={'content-type': 'application/json'}).content.decode("UTF-8")
        return_val = json.loads(request)

        if "token" and "username" in return_val:
            return True,  return_val["token"], return_val["username"]
        else:
            return False

    def Logout(self,username, token ,userid):
        '''
            Logout a user from website
        '''
        request = requests.get(f"{self.url}/tb-logout/{username}/{token}/{userid}/").content.decode("UTF-8")

        if "done" in json.loads(request):
            return True
        else:
            return False
    
    def Create(self, token, name, detail, time):
        '''
            Request in order to create task
        '''
        raw_data = {"name": name ,"detail": detail,"time_to_start": time}
        request = requests.post(f"{self.url}/create/{token}/",
                                json= raw_data, headers= {'content-type': 'application/json'}).content.decode("UTF-8")

        response = json.loads(request)                      
        if "token" in response:
            return True, response["token"]
        else:
            return False

    def Update(self, task_token, user_token):
        '''
            send a Request in order to update a tasks status
        '''
        request = requests.get(f"{self.url}/update/{task_token}/{user_token}/").content.decode("utf-8") 
        
        try:
            response = json.loads(request)
            if "done" in response:
                return True
        except:
            return False



    def Detail(self, user_token, task_token):
        '''
            Request in order to get more detail about a task
        '''
        # send request
        request = requests.get(f"{self.url}/detail/{task_token}/{user_token}/").content.decode("utf-8")
        response = json.loads(request)

        if response != []:
            return response[0]["name"], response[0]["detail"], response[0]["time_to_start"], response[0]["done"]

        else:
            return False


    def Delete(self, user_token, task_token):
        '''
            Delete a task from your list
        '''
        # Send request
        request = requests.get(f"{self.url}/delete/{task_token}/{user_token}/").content.decode("utf-8")

        if "Task  deleted" in request:
            return True
        else:
            return False

    def List(self, token):
        '''
            Request in order to get all tasks of a user
        '''
        request = requests.get(f"{self.url}/list/{token}/").content.decode("utf-8") 
        data = json.loads(request)
        # get the data
        if data == []:
            return False
        
        #if user have tasks
        else:
            task = []

            for response in data:
                # get the tasks and add it to task list
                s = json.loads(json.dumps(response))            
                text = f"name: {s['name']}\ntoken: {s['token']}\nstatus: {s['done']}\n\n"
                task.append(text)

            # write  task list content in a file
            (f := BytesIO(str('\n'.join(task)).encode())).name = 'tasks.txt'
            
            # clear task list
            task.clear()
            return f

    def AutoRemove(self, owner_token):
        '''
            Remove  tasks that have been done 
        '''
        request = requests.get(f"{self.url}/auto-delete/{owner_token}/").content.decode("utf-8")
        
        if "some tasks removed" in request:
            return True

        else:
            return False