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
            self.cursor = self.conn.cursor(buffered=True)

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
            # returns emp_id and emp_password of a given emp
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

    def getEmpId(self, caller = None, email = None):
        if caller == 'E':
            query = "select emp_id from employee where emp_email=%s"
            try:
                self.cursor.execute(query, (email,  ))
                return self.cursor.fetchone()[0]
            except:
                return None

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

    def addEmpToWork(self, prId, empId):
        query = "insert into work (pr_id, emp_id) values (%s, %s)"
        try:
            self.cursor.execute(query, (prId, empId))
            self.conn.commit()
            return 1
        except:
            return 0

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
            # Return the total number of Admin in the organisation (This doesnot include Super Admins)
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

    def getManagerList(self):
        # return all manager ids
        query = "select emp_id from project"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except:
            return None
               
    def getEmployeesEligible(self, org_id, caller=None):
        if caller in ['S', 'P', 'M']:
            # returns all employee from the given org_id
            query = "select t1.emp_id, t1.emp_email, t2.adm_type, t1.emp_name from employee t1 left join admin t2 on t1.emp_id = t2.emp_id where org_id = %s"
            try:
                self.cursor.execute(query, (org_id, ))
                return self.cursor.fetchall()
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

    def getAdm(self, orgId=None, caller = None):
        if caller is None:
            query = "select t1.adm_id, t2.emp_email, t2.emp_name from admin t1 inner join employee t2 on t1.emp_id = t2.emp_id WHERE t2.org_id = %s AND t1.adm_type='A'"

            try:
                self.cursor.execute(query, (orgId, ))
                return self.cursor.fetchall()
            except:
                return None

    def removeAdm(self, admId=None, caller=None):
        if caller is None:
            query = "DELETE FROM admin WHERE adm_id = %s"
            try:
                self.cursor.execute(query, (admId, ))
                self.conn.commit()
                return 1
            except: return 0

    def removeProjFromDB(self, prName):
        query = "delete from project where pr_name = %s"
        try:
            self.cursor.execute(query, (prName, ))
            self.conn.commit()
            return 1
        except:
            return 0

    def addProjToWork(self, empId, prName):
        query1 = "select pr_id from project where pr_name = %s"
        query2 = "INSERT INTO work (emp_id, pr_id) VALUES (%s, %s)"
        try: 
            self.cursor.execute(query1, (prName, ))
            prId = self.cursor.fetchone()[0]
            self.cursor.execute(query2, (empId, prId))
            self.conn.commit()
            return 1
        
        except:
            return 0

    def createProjectinDb(self, prName, manId):
        query =  "INSERT INTO project (pr_name, emp_id) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (prName, manId))
            self.conn.commit()

            return 1
        
        except: return 0

    def getProjectList(self, orgId=None, empId=None, caller=None):
        if caller is None:
            # return all the projects of that organisation
            query = "select t1.pr_id, t1.pr_name, t2.emp_name, t2.emp_id from project t1 left join employee t2 on t1.emp_id = t2.emp_id where t2.org_id=%s"
            try:
                self.cursor.execute(query,(orgId, ))
                return self.cursor.fetchall()
            except:
                return None

        elif caller == 'M':
            # returns the project for which emp_id is the manager
            query = "select pr_id, pr_name from project where emp_id=%s"
            try:
                self.cursor.execute(query, (empId, ))
                return self.cursor.fetchall()
            except:
                return None

    def editWorkEmp(self, prId, oldEmpId, newEmpId):
        query = "update work set emp_id = %s where pr_id=%s and emp_id=%s"
        try:
            self.cursor.execute(query, (newEmpId, prId, oldEmpId))
            self.conn.commit()
            return 1
        
        except: return 0

    def editProjectInDb(self, prId, newProjName=None, newManId=None):

        if newManId is None and newProjName is None:
            return 1
        
        elif newProjName is None:
            query = "update project set emp_id = %s where pr_id = %s"
            try:
                self.cursor.execute(query, (newManId, prId))
                self.conn.commit()
                return 1
            except: return 0
            
        elif newManId is None:
            query = "update project set pr_name = %s where pr_id = %s"
            try:
                self.cursor.execute(query, (newProjName, prId))
                self.conn.commit()
                return 1
            except: return 0

        else:
            query = "update project set pr_name = %s, emp_id = %s where pr_id = %s"
            try:
                self.cursor.execute(query, (newProjName, newManId, prId))
                self.conn.commit()
                return 1
            except: return 0

    def isManager(self, email):
        query = "select 1 from employee t1 left join project t2 on t1.emp_id = t2.emp_id where t1.emp_email=%s"

        self.cursor.execute(query, (email,))
        if self.cursor.fetchone():  return True
        else: return False

    def getEmpInProj(self, prId):
        query = "select t1.emp_id, t1.emp_name, t1.emp_email from employee t1 right join work t2 on t1.emp_id = t2.emp_id where t2.pr_id = %s"
        try:
            self.cursor.execute(query, (prId, ))
            return self.cursor.fetchall()
        except:
            return 0

    def removeEmpFromWork(self, prId, empId):
        query = "delete from work where pr_id = %s and emp_id = %s"
        try:
            self.cursor.execute(query, (prId, empId))
            self.conn.commit()
            return 1
        except:
            return 0

    def getSuppTicketData(self, what):
        if what == 'priority':
            query = "select * from tickets_priority"
        elif what == 'type':
            query = "select * from tickets_type"
        elif what == 'status':
            query = "select * from tickets_status"

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            return None

    def getIndiviadualStatus(self, status):
        query = "select id from tickets_status where status=%s"
        self.cursor.execute(query, (status, ))
        return self.cursor.fetchone()[0]

    def getProjName(self, prId):
        query = "select pr_name from project where pr_id=%s"
        try:
            self.cursor.execute(query, (prId, ))
            return self.cursor.fetchone()[0]
        except:
            return 0

    def getLastTicketId(self, prId):
        query = "select id from ticket where pr_id = %s ORDER BY id DESC LIMIT 1"
        try:
            self.cursor.execute(query, (prId, ))
            return self.cursor.fetchone()
        except Exception as e:
            return None

    def createTicketInDb(self, ticketId, prId, title, ticketType, createdBy, assignee, priority, status,resolvedDate=None, description=None):

        if resolvedDate != 1:

            resolvedDate = None
            query = "insert into ticket (ticket_id, pr_id, title, description, ticket_type, created_by, resolved_date, assignee, priority, ticket_status) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        elif resolvedDate == 1:

            query = "insert into ticket (ticket_id, pr_id, title, description, ticket_type, created_by, assignee, priority, ticket_status, resolved_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"

        try:
            self.cursor.execute(query, (ticketId, prId, title, description, ticketType, createdBy, assignee, priority, status))
            self.conn.commit()
            return 1
        except Exception as e:
            return None

    def getAllTickets(self, prId):
        query = "select id, title, description from ticket where pr_id = %s"
        self.cursor.execute(query, (prId, ))
        return self.cursor.fetchall()

    def getTicketDetails(self, ticketId):
        query  = "select t1.ticket_id, t1.title, t2.pr_name, t7.type, t5.priority, t6.status, t1.description, t3.emp_name as assignee, t4.emp_name as created_by, t1.created_date, t1.modified_date, t1.resolved_date from ticket t1 left join project t2 on t1.pr_id = t2.pr_id left join employee t3 on t1.assignee = t3.emp_id left join employee t4 on t1.created_by = t4.emp_id left join tickets_priority t5 on t1.priority=t5.id left join tickets_status t6 on t1.ticket_status=t6.id left join tickets_type t7 on t1.ticket_type=t7.id where t1.id=%s"
        try: 
            self.cursor.execute(query, (ticketId, ))
            return self.cursor.fetchall()
        except:
            return None