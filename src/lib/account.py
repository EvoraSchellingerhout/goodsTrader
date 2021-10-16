import json


class account():

    def __init__(self, username, token, cash, transport):
        self.username = username
        self.token = token
        self.cash = cash
        self.transport = json.loads(transport)
    

