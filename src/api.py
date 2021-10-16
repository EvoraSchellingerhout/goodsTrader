import lib.game as game
from flask import Flask
from flask_restful import Resource, Api, reqparse

#Begin flask api instance
app = Flask(__name__)
api = Api(app)

#set admin token and initilize game instance
gameAdminToken = "github"
gameInstance = game.game(gameAdminToken)

#setup the argument paerser for api usage
parser = reqparse.RequestParser()
parser.add_argument("token", type=str, help='Unique token used for each account')

#sets the account class
class account(Resource):

    #attempts to register a new account with username
    def post(self, username):
        return gameInstance.createAccount(username)
    
    #attempts to get a users info with username and secure token
    def get(sefl, username):
        args = parser.parse_args()
        userToken = args['token']
        return gameInstance.getAccountInfo(username, userToken)

class admin(Resource):

    def post(self, adminToken):
        if adminToken == gameAdminToken:
            gameInstance.tick()
    
#Creates the account pathing for the api
api.add_resource(account, '/account/<string:username>')
api.add_resource(admin, '/admin/<string:adminToken>')

#enables developer mode (TURN OFF IN PROD!!!)
if __name__ == '__main__':
    app.run(debug=True)