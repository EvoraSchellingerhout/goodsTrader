

class transport:

    def __init__(self, transToken, inventory, inventoryMax, speed, rLoc, tLoc, status):
        self.transToken = transToken
        self.inventory = inventory
        self.inventoryMax = inventoryMax
        self.speed = speed
        self.rLoc = rLoc
        self.tLoc = tLoc
        self.status = status
    
    def isInNode(self, node):
        if self.rLoc == node.rLoc and self.tLoc == node.tLoc:
            return True
        else:
            return False
    
    
        