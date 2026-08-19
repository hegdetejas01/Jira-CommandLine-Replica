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
            self.cursor = self.conn.cursor()

        except mysql.connector.Error as err:
            self.conn = None

    def addOrgToDb(self, name):
        query = "SELECT 1 FROM organisation WHERE org_name = %s LIMIT 1"
        self.cursor.execute(query, (name, ))
        exists = self.cursor.fetchone()
        if exists:
            return 0
        else: 
            try:
                query = "INSERT INTO organisation (org_name) VALUES (%s)"
                self.cursor.execute(query, (name, ))
                self.conn.commit()
                return 1

            except:
                return -1

    def checkEmpinDb(self, email):
        query = "SELECT 1 FROM employee WHERE emp_email = %s LIMIT 1"
        self.cursor.execute(query, (email, ))
        exists = self.cursor.fetchone()
        if exists:
            return 1
        else:
            return 0

    def getPassword(self, email:str):
        query = "SELECT emp_password FROM employee WHERE emp_email = %s"
        self.cursor.execute(query, (email, ))
        return self.cursor.fetchone()[0]

    def getOrg(self):
        query = "SELECT org_id as id, org_name FROM organisation ORDER BY id ASC"
        self.cursor.execute(query)
        return self.cursor

    def addEmpToDb(self, name:str, email:str, password:str, orgNum:int):
        try:
            query = "INSERT INTO employee (emp_name, emp_email, emp_password, org_id) VALUES (%s, %s, %s, %s)"
            insertTuple = (name, email, password, orgNum)
            self.cursor.execute(query, insertTuple)
            self.conn.commit()
            return 1
        except:
            return 0

