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

    def setLoginDateTime(self, email):
        """
        Updates the last login time of the employee
        """
        query = "UPDATE employee SET emp_lastlogin = NOW() WHERE emp_email = %s"
        try:
            self.cursor.execute(query, (email, ))
            self.conn.commit()
        except:
            pass

    def checkEmpinDb(self, org_id=None ,email=None, caller = None):
        if caller is None:
            # Returns all employee data
            query = "SELECT emp_id, emp_password FROM employee WHERE emp_email = %s"
            self.cursor.execute(query, (email, ))
            empData = self.cursor.fetchone()
            return empData

        elif caller=='S':
            # Returns the count of employee
            query = "select count(*) from employee where org_id = %s"
            try:
                self.cursor.execute(query, (org_id, ))
                exists = self.cursor.fetchone()[0]
                return exists
            except:
                return None

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

    def getOrg(self, caller = None, email = None):
        if caller is None:
            query = "SELECT org_id as id, org_name FROM organisation ORDER BY id ASC"
            self.cursor.execute(query)
            return self.cursor

        elif caller == 'E':
            query = "SELECT org_id FROM employee WHERE emp_email = %s"
            try:
                self.cursor.execute(query, (email, ))
                exists = self.cursor.fetchone()[0]
                return exists
            except:
                return None

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

    def checkAdminsInDB(self, org_id=None, email=None, caller=None):
        if caller is None:
            try:
                query = "SELECT COUNT(*) FROM employee WHERE org_id = (SELECT org_id FROM employee WHERE emp_email = %s)"
                self.cursor.execute(query, (email, ))
                exists = self.cursor.fetchone()[0]
                if exists == 1:
                    return 1
                else:
                    return 0
            except:
                return 0

        elif caller == 'S':
            query = "select count(*) from admin t1 inner join employee t2 on t1.emp_id = t2.emp_id WHERE t2.org_id = %s AND t1.adm_type='A'"
            try:
                self.cursor.execute(query, (org_id, ))
                exists = self.cursor.fetchone()[0]
                return exists
            except:
                return None

    def addAdms(self, emp_id):
        try:
            query = "INSERT INTO admin (adm_type, emp_id) VALUES ('A', %s)"
            self.cursor.execute(query, (emp_id, ))
            self.conn.commit() 
            return 1
        except:
            return None
        
    def getEmployeesEligibleAdmin(self, org_id):
        query = "select t1.emp_id, t1.emp_email, t2.adm_type from employee t1 left join admin t2 on t1.emp_id = t2.emp_id where org_id = %s"
        try:
            self.cursor.execute(query, (org_id, ))
            return self.cursor
        except:
            return None

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