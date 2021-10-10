import json
import sqlite3
import secrets
import lib.account
from lib.prettyJson import printPretty
from sqlite3 import Error
from sqlite3.dbapi2 import connect

def createConnection(path):
    tempConnection = None

    try:
        tempConnection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The drror {e} has occured")

    return tempConnection

def executeQuery(con, query, parameters=()):
    cursor = con.cursor()
    try:
        cursor.execute(query, parameters)
        con.commit()
    except Error as e:
        print(f"The drror {e} has occured")


def printQuery(dbConnection, query, parameters=[]):
    cursor = dbConnection.cursor()
    result = None

    try:
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        print("got Here")
        return result
    except Error as e:
        print(f"The drror {e} has occured")

def genAccountToken():
    return secrets.token_hex(16)

class game:

    def __init__(self):
        self.loadDatabases()


    def loadDatabases(self):
        self.dbConnection = createConnection("data/main.sqlite")

        self.loadNodeDB()
        self.loadGoodsDB()
        self.loadAccountDB()

    def loadNodeDB(self):
        createNodeTable = """
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rate INTEGER,
            name TEXT NOT NULL,
            TYPE INTEGER NOT NULL,
            xLoc INTEGER,
            yLoc INTEGER
        );
        """
        executeQuery(self.dbConnection, createNodeTable)
    
    def loadGoodsDB(self):
        createGoodsTable = """
        CREATE TABLE IF NOT EXISTS goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
        executeQuery(self.dbConnection, createGoodsTable)

    def loadAccountDB(self):
        createAccountTable = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            userToken TEXT NOT NULL,
            cash INTEGER 
        );
        """
        executeQuery(self.dbConnection, createAccountTable)
    
    def createAccount(self, username):
        username = str(username)
        tempToken = genAccountToken()

        accountSearchQuery = "SELECT * FROM accounts"
        searchResults = printQuery(self.dbConnection, accountSearchQuery)
        print(searchResults)
        for account in searchResults:
            if account[1] == username:
                return {"Error": "Username already taken"}
            if account[2] == tempToken:
                tempToken = genAccountToken()

        accountCreationQuery = f"""
        INSERT INTO
            accounts (username, userToken, cash)
        VALUES
            ( ?, ?, 100000)
        """
        #print(accountCreationQuery)

        executeQuery(self.dbConnection, accountCreationQuery, (username, tempToken))
        
        returnDict = {
            "User": {
                "username": username,
                "userToken": tempToken,
                "cash": 100000
            }
        }
        return returnDict

    def getAccount(self, username, userToken):
        accountSearchQuery = "SELECT * FROM accounts WHERE username = (?)"
        searchResults = printQuery(self.dbConnection, accountSearchQuery, [username,])[0]
        print(searchResults)
        if searchResults[2] == userToken:
            accountDict = {
                "User": {
                    "username": searchResults[1],
                    "token": searchResults[2],
                    "cash": searchResults[3] 
                }
            }
            return accountDict
        else:
            returnDcit = {
                "Error": f"Token not valid for {username}"
            }
            return returnDcit



testGame = game()
testAccount = lib.account.account('test', 'test', 10)