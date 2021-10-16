
class node:

    def __init__(self, name, type, rate, cost, symbol, inventory, inventoryMax, rLoc, tLoc, prodInventory=None):
        self.name = name
        self.type = type
        self.rate = rate
        self.cost = cost
        self.symbol = symbol
        self.inventory = inventory
        self.inventoryMax = inventoryMax
        self.rLoc = rLoc
        self.tLoc = tLoc
        if prodInventory != None:
            self.prodInventory = prodInventory
    
    def superInitilize(self):
        self.inventory = self.rate * 24
    
    def updateNodeEntry(self):
        nodeUpdateQuery = f"""
        UPDATE nodes
        SET inventory = (?)
        WHERE symbol = (?)
        """
        return nodeUpdateQuery

    def tick(self):
        if self.type == 1:
            #print("node Ticked")
            if (self.inventory + self.rate) >= self.inventoryMax:
                self.inventory = self.inventoryMax
            else:
                self.inventory = self.inventory + self.rate
        if self.type == 2:
            pass
        if self.type == 3:
            #print("node Ticked")
            self.inventory = self.inventory - self.rate
        return self.updateNodeEntry()

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
                "inventoryMax": self.inventoryMax
            }
        }
        return tempDict
    

    def purchase(self, amount):
        self.inventory = self.inventory - amount
        