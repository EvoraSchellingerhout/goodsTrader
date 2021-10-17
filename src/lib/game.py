import sqlite3
import secrets
import random
import lib.GTDatabase as GTDatabase
import lib.nodes as nodes




class game:

    def __init__(self, adminToken):
        self.adminToken = adminToken
        self.DB = None
        self.initilizeDatabases()
        self.nodeDict = {}
        self.nodeDict = self.generateNodes(100)
    
    def tick(self):
        for node in self.nodeDict:
            nodeUpdateQuery = self.nodeDict[node]['node'].tick()
            self.DB.executeQuery(nodeUpdateQuery, [self.nodeDict[node]['node'].inventory, self.nodeDict[node]['symbol']])
        print("Tick Succesful")

    def initilizeDatabases(self):
        self.DB = GTDatabase.GTDatabase("data/main.sqlite")
        
        self.initAccountDB()
        self.initNodeDB()
        self.initTransDB()
    
    def initAccountDB(self):
        createAccountTableQuery = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            userToken TEXT NOT NULL,
            cash INTEGER
        );
        """

        self.DB.executeQuery(createAccountTableQuery)
    
    def initNodeDB(self):
        createNodeTableQuery = """
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
        self.DB.executeQuery(createNodeTableQuery)

    def initTransDB(self):
        createTransTableQuery = """
        CREATE TABLE IF NOT EXISTS transports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userToken TEXT NOT NULL,
            transToken TEXT NOT NULL,
            inventory INTEGER NOT NULL,
            invMax INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            rLoc INTEGER NOT NULL,
            tLoc INTEGER NOT NULL,
            status TEXT NOT NULL
        );
        """
        self.DB.executeQuery(createTransTableQuery)

    def createAccount(self, username):
        username = str(username)
        tempToken = secrets.token_hex(16)
        accountSearchQuery = "SELECT * FROM accounts"
        searchResults = self.DB.printQuery(accountSearchQuery)
        for account in searchResults:
            if account[1] == username:
                return {"Error": "Username already taken"}
            if account[2] == tempToken:
                tempToken = secrets.token_hex(16)

        accountCreationQuery = """
        INSERT INTO
            accounts (username, userToken, cash)
        VALUES
            ( ?, ?, 100000)
        """
        #print(accountCreationQuery)

        self.DB.executeQuery(accountCreationQuery, [username, tempToken])
        
        returnDict = {
            "User": {
                "username": username,
                "userToken": tempToken,
                "cash": 100000,
                "transports": []
            }
        }
        return returnDict

    def getAccountTrans(self, userToken):
        transSearchQuery = "SELECT * FROM transports WHERE userToken = (?)"
        parameters = [userToken]
        searchResults = self.DB.printQuery(transSearchQuery, parameters)
        tempTransList = [ ]
        if searchResults == None:
            return tempTransList
        else:
            for tran in searchResults:
                tempTransList.append(tran[2])
            return tempTransList

    def getAccountInfo(self, userToken):
        accountSearchQuery = "SELECT * FROM accounts WHERE userToken = (?)"
        parameters = [userToken]
        searchResults = self.DB.printQuery(accountSearchQuery, parameters)
        if searchResults == None:
            return {"Error": f"UserToken does not exist"}
        else:
            searchResults = searchResults[0]
            return {
                "User": {
                    "username": searchResults[1],
                    "userToken": searchResults[2],
                    "cash": searchResults[3],
                    "transports": self.getAccountTrans(userToken)
                }
            }
    
    def accountUpdate(self, userToken, newCash):
        updateAccountQuery = f"""
        UPDATE accounts
        SET
            cash = {newCash}
        WHERE
            userToken = (?)
        """
        parameters = [userToken]
        self.DB.executeQuery(updateAccountQuery, parameters)
    
    def createNewTrans(self, userToken):
        transInsertQuery = """
        INSERT INTO
            transports (userToken, transToken, inventory, invMax, speed, rLoc, tLoc, status)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
        
        """
        parameters = [
            userToken,
            secrets.token_hex(16),
            0,
            1000,
            1,
            0,
            0,
            "Stopped"
        ]

        self.DB.executeQuery(transInsertQuery, parameters)
        
    def purchaseTransport(self, userToken):
        userSearchQuery = "SELECT * FROM accounts WHERE userToken = (?)"
        parameters = [userToken]
        searchResults = self.DB.printQuery(userSearchQuery, parameters)
        print(searchResults)
        if searchResults == None:
            return {"Error": "UserToken does not exist"}
        else:
            searchResults = searchResults[0]
            if searchResults[3] >= 10000:
                self.createNewTrans(userToken)
                self.accountUpdate(userToken, searchResults[3] - 10000)
                return self.getAccountInfo(userToken)
            else:
                return {"Error": "Not enough cash"}
    
    def getTrans(self, userToken, transToken):
        transSearchQuery = "SELECT * FROM transports WHERE transToken = (?)"
        parameters = [transToken]
        searchResults = self.DB.printQuery(transSearchQuery, parameters)
        #print(searchResults)
        if searchResults == None or searchResults == []:
            return {"Error": "Transport does not exist"}
        else:
            searchResults = searchResults[0]
            return {
                "Transport": {
                    "userToken": searchResults[1],
                    "id": searchResults[2],
                    "inventory": searchResults[3],
                    "maxInventory": searchResults[4],
                    "speed" : searchResults[5],
                    "rLoc": searchResults[6],
                    "tLoc": searchResults[7],
                    "status": searchResults[8],
                }
            }
    
    def getAllTrans(self, userToken):
        transSearchQuery = "SELECT * FROM transports WHERE userToken = (?)"
        parameters = [userToken]
        searchResults = self.DB.printQuery(transSearchQuery, parameters)
        #print(searchResults)
        if searchResults == None:
            return {"Error": "Either Token is bad or no transports exist for the account"}
        else:
            tranDict = {}
            for tran in searchResults:
                tempTranDict = {
                    tran[2]: {
                        "id": tran[2],
                        "inventory": tran[3],
                        "maxInventory": tran[4],
                        "speed": tran[5],
                        "rLoc": tran[6],
                        "tLoc": tran[7],
                        "status": tran[8]
                    }
                }
                print(tempTranDict)
                tranDict = {**tempTranDict, **tranDict}
            #print(tranDict)
            return tranDict
    
    def transTravel(self, userToken, transToken):
        tranSearchQuery = "SELECT * FROM transports WHERE transToken = (?) AND userToken = (?)"
        parameters = [transToken, userToken]
        searchResults = self.DB.printQuery(tranSearchQuery, parameters)
        if searchResults == None or searchResults == []:
            return {"Error": "UserToken or transToken is invalid"}
        else:
            searchResults = searchResults[0]
    
    """tempDict = {
            self.symbol: {
                "node": self,
                "name": self.name,
                "type": self.type,
                "rate": self.rate,
                "cost": self.cost,
                "symbol": self.symbol,
                "inventory": self.inventory,
                "inventoryMax": self.inventoryMax
            }
        }"""
    "(self, name, type, rate, cost, symbol, inventory, inventoryMax, rLoc, tLoc, prodInventory=None)"
    def genHUBNode(self):
        HUBNode = nodes.node("H.U.B", -1, 0, 0, "HUB", 0, 0, 0, 0)
        HUBDIct = {
            HUBNode.symbol: {
                "node": HUBNode,
                "name": HUBNode.name,
                "type": HUBNode.type,
                "cost": HUBNode.cost,
                "symbol": HUBNode.symbol,
                "inventory": HUBNode.inventory,
                "inventoryMax": HUBNode.inventoryMax
            }
        }

        return HUBDIct
    
    def readInNodes(self):
        nodeRetrivalQuery = "SELECT * from nodes"
        nodeList = self.DB.printQuery(nodeRetrivalQuery)
        tempNodeDict = {}
        for retrieved in nodeList:
            tempNode = nodes.node(retrieved[1], retrieved[2], retrieved[3], retrieved[4], retrieved[5], int(retrieved[6]), int(retrieved[7]), retrieved[8], retrieved[9])
            tempRetrivalDict = tempNode.printNodeDict()
            tempNodeDict = {**tempRetrivalDict, **tempNodeDict}
        return tempNodeDict
    
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

        self.DB.executeQuery(initilizeNodeQuery, parameters)
    
    def generateNode(self):
        name = "".join(random.choice('AEIOUY')).join(random.choice('aeiouy') for _ in range(random.randint(2, 6)))
        type = (random.randint(0, 1) * 2) + 1
        rate = random.randint(500, 5000)
        cost = 20
        symbol = secrets.token_hex(4)
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
        nodeCount = self.DB.printQuery(checkNodeDBQuery)[0][0]
        tempNodeDict = {}
        if nodeCount == None:
            nodeCount = 0
        else:
            nodeCount = int(nodeCount)
            tempNodeDict = self.readInNodes()
        if genNum - nodeCount > 0:
            for i in range(genNum - nodeCount):
                tempNodeDict = {**self.generateNode(), **tempNodeDict}
        tempNodeDict = {**self.genHUBNode(), **tempNodeDict}
        return tempNodeDict        