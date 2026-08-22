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

        except:
            self.conn = None

    def addOrgToDb(self, name):
        """
        Returns 0 if exists - login page
        Returns 1 if successfully registered - login page
        returns -1, if failed to register - register page
        """
        query = "SELECT 1 FROM organisation WHERE org_name = %s"
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
        query = "SELECT emp_id, emp_password FROM employee WHERE emp_email = %s"
        self.cursor.execute(query, (email, ))
        empData = self.cursor.fetchone()
        return empData

    def checkEmpinAdm(self, empId):
        """
        Returns S E or A based on who has logged in
        """
        query = "SELECT 1 FROM admin WHERE emp_id = %s and adm_type = %s"
        self.cursor.execute(query, (empId, 'S'))
        existsSuper = self.cursor.fetchone()
        if existsSuper: 
            return 'S'
        else: 
            query = "SELECT 1 FROM admin WHERE emp_id = %s and adm_type = %s"
            self.cursor.execute(query, (empId, 'A'))
            existsAdm = self.cursor.fetchone()
            if existsAdm: 
                return 'A'
            else: 
                return 'E'
        
            

    def getPassword(self, email:str):
        query = "SELECT emp_password FROM employee WHERE emp_email = %s"
        self.cursor.execute(query, (email, ))
        return self.cursor.fetchone()[0]

    def getOrg(self):
        query = "SELECT org_id as id, org_name FROM organisation ORDER BY id ASC"
        self.cursor.execute(query)
        return self.cursor

    def addEmpToDb(self, name:str, email:str, password:str, orgNum:int):
        """
        Returns 1 for successfully adding to DB, else 0
        """
        try:
            query = "INSERT INTO employee (emp_name, emp_email, emp_password, org_id) VALUES (%s, %s, %s, %s)"
            insertTuple = (name, email, password, orgNum)
            self.cursor.execute(query, insertTuple)
            self.conn.commit()
            return 1
        except:
            return 0

    def checkAdminsInDB(self, emp_email):
        """
        Returns 1 if employee has to be added as super admin, else 0
        """
        try:
            query = "SELECT COUNT(*) FROM employee WHERE org_id = (SELECT org_id FROM employee WHERE emp_email = %s)"
            self.cursor.execute(query, (emp_email, ))
            exists = self.cursor.fetchone()[0]
            if exists == 1:
                return 1
            else:
                return 0
        except:
            return 0

    def addAdminToDb(self, email, adminType):
        """
        Returns 1 if employee is successfully added as Super Admin, else 0
        """
        try:
            query = "SELECT emp_id FROM employee WHERE emp_email = %s"
            self.cursor.execute(query, (email, ))
            empId = self.cursor.fetchone()[0]

            query = "INSERT INTO admin (adm_type, emp_id) VALUES (%s, %s)"
            insertTuple = (adminType, empId)
            self.cursor.execute(query, insertTuple)
            self.conn.commit() 

            return 1

        except:
            return 0