import json
import sqlite3
import secrets
import random
import lib.account as account
import lib.nodes as nodes
from lib.prettyJson import printPretty
from sqlite3 import Error
from sqlite3.dbapi2 import connect


#create a cnnection given a path
def createConnection(path):
    tempConnection = None

    #Attempts to connect throws error if unable
    try:
        tempConnection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The drror {e} has occured")
        return False

    #returns tempConnection if no error
    return tempConnection

#attempts to execute the query with the given parameters
def executeQuery(con, query, parameters=[]):
    cursor = con.cursor()

    #attemps to execute the command
    try:
        cursor.execute(query, parameters)
        con.commit()
    except Error as e:
        print(f"The drror {e} has occured")
        return False

#attempts to print the query results with the given parameters
def printQuery(dbConnection, query, parameters=[]):
    cursor = dbConnection.cursor()
    result = None

    #tried to execute the query
    try:
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The drror {e} has occured")
        return False

#generates the unique token for each account
def genAccountToken(byteLength):
    return secrets.token_hex(byteLength)

"""
Class: Game
initArgs: adminToken
    adminToken: Token used to access admin commands, stored in api.py
Purpose: Hosts the game instance and is the base for all other actions involving
Nodes, Goods, Accounts
"""
class game:

    def __init__(self, adminToken):
        self.loadDatabases()
        self.adminToken = adminToken
        self.nodeDict = self.generateNodes(100)
        #self.startGameLoop()
        #print(self.nodeDict)

    """     
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            TYPE INTEGER NOT NULL,
            rate INTEGER,
            cost INTEGER,
            symbol TEXT NOT NULL,
            inventory TEXT NOT NULL,
            invmax TEXT NOT NULL,
            rLoc INTEGER,
            tLoc INTEGER
    """

    '''(self, name, type, rate, cost, symbol, inventory, inventoryMax, rLoc, tLoc, prodInventory=None)'''

    def tick(self):
        #print(self.nodeDict)
        #print("tick succesful")
        for node in self.nodeDict:
            #print(node)
            nodeUpdateQuery = self.nodeDict[node]['node'].tick()
            executeQuery(self.dbConnection, nodeUpdateQuery, [self.nodeDict[node]['inventory'], self.nodeDict[node]['symbol']])
        print("Tick Succesful")

    def initilizeNode(self, newNode):
        initilizeNodeQuery = """
        INSERT INTO
            nodes (name, type, rate, cost, symbol, inventory, invmax, rloc, tloc)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = [
            newNode.name,
            newNode.type,
            newNode.rate,
            newNode.cost,
            newNode.symbol,
            newNode.inventory,
            newNode.inventoryMax,
            newNode.rLoc,
            newNode.tLoc
        ]

        executeQuery(self.dbConnection, initilizeNodeQuery, parameters)
    
    def readInNodes(self):
        nodeRetrivalQuery = "SELECT * from nodes"
        nodeList = printQuery(self.dbConnection, nodeRetrivalQuery)
        tempNodeDict = {}
        for retrieved in nodeList:
            #print(retrieved)
            """tempRetrivalDict = {
                "name": retrieved[1],
                "type": retrieved[2],
                "rate": retrieved[3],
                "cost": retrieved[4],
                "symbol": retrieved[5],
                "inventory": retrieved[6],
                "invmax": retrieved[7],
                "rLoc": retrieved[8],
                "tLoc": retrieved[9],
            }
            """
            tempNode = nodes.node(retrieved[1], retrieved[2], retrieved[3], retrieved[4], retrieved[5], int(retrieved[6]), int(retrieved[7]), retrieved[8], retrieved[9])
            tempRetrivalDict = tempNode.printNodeDict()
            tempNodeDict = {**tempRetrivalDict, **tempNodeDict}
        return tempNodeDict

    def genHUBNode(self):
        HUBNode = nodes.node("H.U.B", -1, 0, 0, "H.U.B", 0, 0, 0, 0)
        return HUBNode.printNodeDict()
        

    def generateNode(self):
        name = "".join(random.choice('AEIOUY')).join(random.choice('aeiouy') for _ in range(random.randint(2, 6)))
        type = (random.randint(0, 1) * 2) + 1
        rate = random.randint(500, 5000)
        cost = 20
        symbol = genAccountToken(4)
        inventoryMax = 5000
        rLoc = random.randint(1, 100)
        tLoc = random.randint(0, 359)
        inventory = random.randint(500, 5000)
        newNode = nodes.node(name, type, rate, cost, symbol, inventory, inventoryMax, rLoc, tLoc)
        newNodeDict = newNode.printNodeDict()
        #print(newNodeDict)
        self.initilizeNode(newNode)
        #print(newNode.printNodeDict())
        return newNodeDict

    def generateNodes(self, genNum):
        checkNodeDBQuery = """SELECT MAX(id) AS max_id
        FROM nodes;"""
        nodeCount = printQuery(self.dbConnection, checkNodeDBQuery)[0][0]
        #print(nodeCount)
        #print(nodeCount)
        tempNodeDict = {}
        if nodeCount == None:
            nodeCount = 0
        else:
            nodeCount = int(nodeCount)
            tempNodeDict = self.readInNodes()
        if genNum - nodeCount > 0:
            for i in range(genNum - nodeCount):
                #print({**self.generateNode(), **tempNodeDict})
                tempNodeDict = {**self.generateNode(), **tempNodeDict}
        tempNodeDict = {**self.genHUBNode(), **tempNodeDict}
        return tempNodeDict



    def loadDatabases(self):
        self.dbConnection = createConnection("data/main.sqlite")

        self.loadNodeDB()
        self.loadAccountDB()

    """name, type, rate, cost, symbol, inventory, invmax, rloc, tloc"""

    def loadNodeDB(self):
        createNodeTable = """
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type INTEGER NOT NULL,
            rate INTEGER,
            cost INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            inventory TEXT NOT NULL,
            invmax TEXT NOT NULL,
            rLoc INTEGER,
            tLoc INTEGER
        );
        """
        executeQuery(self.dbConnection, createNodeTable)
    
    """def loadGoodsDB(self):
        createGoodsTable =
        CREATE TABLE IF NOT EXISTS goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        
        executeQuery(self.dbConnection, createGoodsTable)
        """

    def loadAccountDB(self):
        createAccountTable = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            userToken TEXT NOT NULL,
            cash INTEGER,
            transports TEXT
        );
        """
        executeQuery(self.dbConnection, createAccountTable)
    
    def createAccount(self, username):
        username = str(username)
        tempToken = genAccountToken(16)

        accountSearchQuery = "SELECT * FROM accounts"
        searchResults = printQuery(self.dbConnection, accountSearchQuery)
        #print(searchResults)
        for account in searchResults:
            if account[1] == username:
                return {"Error": "Username already taken"}
            if account[2] == tempToken:
                tempToken = genAccountToken(16)

        accountCreationQuery = """
        INSERT INTO
            accounts (username, userToken, cash, transports)
        VALUES
            ( ?, ?, 100000, \{\})
        """
        #print(accountCreationQuery)

        executeQuery(self.dbConnection, accountCreationQuery, [username, tempToken])
        
        returnDict = {
            "User": {
                "username": username,
                "userToken": tempToken,
                "cash": 100000,
                "transports": []
            }
        }
        return returnDict

    def getAccountInfo(self, username, userToken):
        accountSearchQuery = "SELECT * FROM accounts WHERE username = (?)"
        searchResults = printQuery(self.dbConnection, accountSearchQuery, [username,])[0]
        print(searchResults)
        if searchResults[2] == userToken:
            accountDict = {
                "User": {
                    "username": searchResults[1],
                    "token": searchResults[2],
                    "cash": searchResults[3],
                    "transports": json.loads(searchResults[4]) 
                }
            }
            return accountDict
        else:
            returnDcit = {
                "Error": f"Token not valid for {username}"
            }
            return returnDcit

    def getAccount(self, userToken):
        accountSearchQuery = "SELECT * FROM accounts WHERE userToken = (?)"
        searchResults = printQuery(self.dbConnection, accountSearchQuery, [userToken,])[0]
        #print(searchResults)
        if searchResults[2] == userToken:
            accountDict = {
                "User": {
                    "username": searchResults[1],
                    "token": searchResults[2],
                    "cash": searchResults[3],
                    "transports": json.loads(searchResults[4])
                }
            }
            return accountDict
        else:
            returnDcit = {
                "Error": "Token not valid"
            }
            return returnDcit

    def updateAccountPurchase(userToken, cashChange):
        updateQuery = """
        UPDATE
            accounts
        SET
            cash = (?)
        WHERE
            userToken = (?)
        """
        parameters = [cashChange, userToken]
        executeQuery(updateQuery, parameters)


    def purchaseGoods(self, accountToken, nodeSymbol, transportToken, amount):
        tempAccountDict = self.getAccount(accountToken)
        if tempAccountDict.has_key("Error"):
            return tempAccountDict
        for trans in tempAccountDict["User"]["transports"]:
            if trans["transToken"] == transportToken:
                if trans["inventory"] + amount <= trans["inventoryMax"]:
                    if trans["rLoc"] == self.nodeDict[nodeSymbol]['rLoc'] and trans["tLoc"] == self.nodeDict[nodeSymbol]['tLoc']:
                        if self.nodeDict[nodeSymbol]['inventory'] >= amount and self.nodeDict[nodeSymbol]["type"] == 1:
                            if tempAccountDict["User"]["cash"] >= (self.nodeDict[nodeSymbol]["cost"] * amount):
                                self.nodeDict[nodeSymbol]['node'].purchase(amount)
                                cashChange = tempAccountDict["User"]["cash"] - (amount * self.nodeDict[nodeSymbol]['cost'])
                                self.updateAccountPurchase(accountToken, cashChange)

                            else:
                                return {"Error": f"Not enough funds to purchase {amount} goods"}
                        else:
                            return {"Error": "Node does not have enough inventory or is the wrong type"}
                    else:
                        return {"Error": f"Transport is not at {nodeSymbol}"}
                else:
                    return {"Error": f"Not enough invetory in transport {trans['trandToken']}"}
            else:
                return {"Error": f"transportToken is invalid for {tempAccountDict['User']['username']}"}
                

        
        