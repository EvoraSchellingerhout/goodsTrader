import sqlite3


class GTDatabase:

    def __init__(self, path):
        try:
            self.DB = sqlite3.connect(path, check_same_thread=False)
        except sqlite3.Error as e:
            print(f"Error: {e}, has occured durring connection creation")
        
    def executeQuery(self, query, parameters=[]):
        DBCursor = self.DB.cursor()

        try:
            DBCursor.execute(query, parameters)
            self.DB.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}, has occured durring command execution")
            return False

    def printQuery(self, query, parameters=[]):
        DBCursor = self.DB.cursor()
        result = None

        #tried to execute the query
        try:
            DBCursor.execute(query, parameters)
            result = DBCursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error: {e}, has occured durring printing execution")
            return False