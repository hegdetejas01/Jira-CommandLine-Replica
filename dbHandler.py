import mysql.connector

class DbHandler:

    def __init__(self):
        try: 
            conn = mysql.connector.connect(
                user="root", 
                password="",
                host="localhost",
                database="jira_db")
            self.conn = conn

        except mysql.connector.Error as err:
            self.conn = None

    def addOrgToDb(self, name):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM organisation WHERE org_name = %s LIMIT 1"
        cursor.execute(query, (name, ))
        exists = cursor.fetchone()
        if exists:
            return 0
        else: 
            try:
                query = "INSERT INTO organisation (org_name) VALUES (%s)"
                cursor.execute(query, (name, ))
                self.conn.commit()
                return 1

            except:
                return -1