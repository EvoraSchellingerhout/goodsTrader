import math
import lib.GTDatabase as GTDatabase

class node:

    def __init__(self, name, type, rate, baseCost, symbol, inventory, inventoryMax, rLoc, tLoc, prodInventory=None):
        self.name = name
        self.type = type
        self.rate = rate
        self.baseCost = baseCost
        self.symbol = symbol
        self.inventory = inventory
        self.inventoryMax = inventoryMax
        self.rLoc = rLoc
        self.tLoc = tLoc
        if self.type == -1:
            self.cost = 0
        elif self.type == 1 or self.type == 3:
            self.cost = math.floor(self.baseCost ** (1 - (self.inventory / self.inventoryMax)))
        else:
            self.cost = baseCost
        if prodInventory != None:
            self.prodInventory = prodInventory
    
    def superInitilize(self):
        self.inventory = self.rate * 24
        if self.type != -1:
            self.cost = math.floor(self.baseCost ** (1 - (self.inventory / self.inventoryMax)))
    
    def updateNodeEntry(self):
        nodeUpdateQuery = f"""
        UPDATE nodes
        SET inventory = (?),
        WHERE symbol = (?)
        """
        return nodeUpdateQuery

    def tick(self, DB=None):
        if self.type == 1:
            #print("node Ticked")
            if (self.inventory + self.rate) >= self.inventoryMax:
                self.inventory = self.inventoryMax
            else:
                self.inventory = self.inventory + self.rate
        if self.type == 2:
            if DB == None:
                print("Error: No DB for Refine Node")
            else:
                self.refineNodeTick(DB)
        if self.type == 3:
            #print("node Ticked")
            if self.inventory - self.rate >= 0:
                self.inventory = self.inventory - self.rate
        
        if self.type != -1:
            self.cost = math.floor(self.baseCost ** (1 - (self.inventory / self.inventoryMax)))

        return self.updateNodeEntry()

    def refineNodeTick(self, DB: GTDatabase.GTDatabase):
        tempGoodsDeposited = 0
        tempGoodsReady = 0
        refinarySearchQuery = f"SELECT * FROM refinaries WHERE nodeSymbol = {self.symbol}"
        searchResults = DB.printQuery(refinarySearchQuery)
        if searchResults == [] or searchResults == None:
            return False
        else:
            for entry in searchResults:
                tempGoodsDeposited = entry[3]
                tempGoodsReady = entry[4]
                if tempGoodsDeposited <= self.rate:
                    tempGoodsDeposited = 0
                    tempGoodsReady = tempGoodsReady + tempGoodsDeposited
                else:
                    tempGoodsDeposited = tempGoodsDeposited - self.rate
                    tempGoodsReady = tempGoodsReady + self.rate
            return True

    def printNodeDict(self):
        tempDict = {
            self.symbol: {
                "node": self,
                "name": self.name,
                "type": self.type,
                "rate": self.rate,
                "cost": self.cost,
                "symbol": self.symbol,
                "inventory": self.inventory,
                "inventoryMax": self.inventoryMax,
                "rLoc": self.rLoc,
                "tLoc": self.tLoc
            }
        }
        return tempDict

    def printSafeRefNodeDict(self, userToken, DB: GTDatabase.GTDatabase):
        tempGoodsDeposited = 0
        tempGoodsReady = 0
        refSearchQuery = "SELECT * FROM refinaries WHERE nodeSymbol = (?) AND userToken = (?)"
        parameters = [self.symbol, userToken]
        searchResults = DB.printQuery(refSearchQuery, parameters)
        if searchResults == [] or searchResults == None:
            return self.printSafeNodeDict()
        else:
            searchResults = searchResults[0]
            #tempGoodsDeposited = searchResults[3]
            #tempGoodsReady = searchResults[4]
            tempDict = {
                self.symbol: {
                    "name": self.name,
                    "type": self.type,
                    "rate": self.rate,
                    "cost": self.cost,
                    "symbol": self.symbol,
                    "goodsDeposited": searchResults[3],
                    "goodsReady": searchResults[4],
                    "inventoryMax": self.inventoryMax,
                    "rLoc": self.rLoc,
                    "tLoc": self.tLoc
                }
            }
            return tempDict

    def getSafeNodeDict(self, userToken="", DB=None):
        if self.type == 2:
            if userToken == "" or DB == None:
                return self.printSafeNodeDict()
            else:
                return self.printSafeRefNodeDict(self, userToken, DB)
        else:
            return self.printSafeNodeDict()
    
    def printSafeNodeDict(self):
        if self.type == 2:
            tempDict = {
                self.symbol: {
                    "name": self.name,
                    "type": self.type,
                    "rate": self.rate,
                    "cost": self.cost,
                    "symbol": self.symbol,
                    "inventoryMax": self.inventoryMax,
                    "rLoc": self.rLoc,
                    "tLoc": self.tLoc
                }
            }
            return tempDict
        else:
            tempDict = {
                self.symbol: {
                    "name": self.name,
                    "type": self.type,
                    "rate": self.rate,
                    "cost": self.cost,
                    "symbol": self.symbol,
                    "inventory": self.inventory,
                    "inventoryMax": self.inventoryMax,
                    "rLoc": self.rLoc,
                    "tLoc": self.tLoc
                }
            }
            return tempDict
    
    def purchase(self, amount):
        self.inventory = self.inventory - amount
        if self.type != -1:
            self.cost = math.floor(self.baseCost ** (1 - (self.inventory / self.inventoryMax)))
        