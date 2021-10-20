from typing import no_type_check_decorator
import lib.game as game
from flask import Flask
from flask_restful import Resource, Api, reqparse
import time, threading

#Begin flask api instance
app = Flask(__name__)
api = Api(app)

#set admin token and initilize game instance
gameAdminToken = "github"
gameInstance = game.game(gameAdminToken)

#begin tick schedul
def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(10, next_time - time.time()))
    task()
    
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay

threading.Thread(target=lambda: every(60, gameInstance.tick)).start()

#setup the argument paerser for api usage
parser = reqparse.RequestParser()
parser.add_argument("token", type=str, help='Unique token used for each account')
parser.add_argument("symbol", type=str, help="Unique symbol for each node")
parser.add_argument("type", type=int, help="Node type indicator")
parser.add_argument('amount', type=int, help="Amount of good being traded")
parser.add_argument('adminToken', type=str, help="Token used to run admin commands")

#sets the account class
class createAccount(Resource):

    #attempts to register a new account with username
    def post(self, username):
        return gameInstance.createAccount(username)
    
class account(Resource):
    #attempts to get a users info with username and secure token
    def get(self):
        args = parser.parse_args()
        userToken = args['token']
        return gameInstance.getAccountInfo(userToken)

class nodes(Resource):

    def get(self):
        args = parser.parse_args()
        symbol = args["symbol"]
        type = args['type']
        return gameInstance.getNodes(symbol, type)

class genTransports(Resource):
    
    def post(self):
        args = parser.parse_args()
        userToken = args['token']
        return gameInstance.purchaseTransport(userToken)

    def get(self):
        args = parser.parse_args()
        userToken = args["token"]
        return gameInstance.getAllTrans(userToken)

class specificTransports(Resource):
    
    def get(self, transToken):
        args = parser.parse_args()
        userToken = args["token"]
        return gameInstance.getTrans(userToken, transToken)
    
    def post(self, transToken):
        args = parser.parse_args()
        userToken = args['token']
        nodeSymbol = args['symbol']
        return gameInstance.transTravel(userToken, transToken, nodeSymbol)

class transTrade(Resource):

    def get(self, transToken, nodeSymbol):
        args = parser.parse_args()
        userToken = args['token']
        return gameInstance.transTradeCheck(userToken, transToken, nodeSymbol)
    
    def post(self, transToken, nodeSymbol):
        args = parser.parse_args()
        userToken = args['token']
        amount = args['amount']
        return gameInstance.transTrade(userToken, transToken, nodeSymbol, amount)

class admin(Resource):
    pass

class adminNodes(Resource):

    def get(self):
        args = parser.parse_args()
        adminToken = args['adminToken']
        if adminToken == gameAdminToken:
            args = parser.parse_args()
            symbol = args["symbol"]
            type = args['type']
            return gameInstance.getNodesAdmin(symbol, type)
        else:
            return {"Error": "AdminToken is not valid"}

#Creates the account pathing for the api
api.add_resource(createAccount, '/account/create/<string:username>/')
api.add_resource(account, '/account/')
api.add_resource(admin, '/admin/')
api.add_resource(genTransports, '/account/transports/')
api.add_resource(specificTransports, "/account/transports/<string:transToken>/")
api.add_resource(transTrade, '/accounts/transports/<string:transToken>/<string:nodeSymbol>/')
api.add_resource(nodes, "/nodes/")
api.add_resource(adminNodes, "/admin/nodes/")

#enables developer mode (TURN OFF IN PROD!!!)
if __name__ == '__main__':
    app.run(debug=True)