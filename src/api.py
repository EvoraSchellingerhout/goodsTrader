import lib.game as game
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

gameInstance = game.game()

parser = reqparse.RequestParser()
parser.add_argument("token", type=str, help='Unique token used for each account')
"""
class HelloWorld(Resource):
    def get(self):
        return {"Hello": "world"}
    
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

"""

class accountCreation(Resource):

    def post(self, username):
        return gameInstance.createAccount(username)
    
    def get(sefl, username):
        args = parser.parse_args()
        userToken = args['token']
        return gameInstance.getAccount(username, userToken)
    

api.add_resource(accountCreation, '/account/<string:username>')


if __name__ == '__main__':
    app.run(debug=True)