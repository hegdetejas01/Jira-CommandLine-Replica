from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator

class Employee:
    
    def registerEmployee(self, dbHandlerObj: DbHandler):
        self.email = input(ps.empRegEmail)
        response = dbHandlerObj.checkEmpinDb(self.email)
        if response:
            print(ps.empPresent)
        else:
            name = input(ps.empRegName)
            pass_ = input(ps.empRegPassword)
            cursor = dbHandlerObj.getOrg()
            print(ps.askOrg)
            for o_id, o_name in cursor:
                print("Click {} for {}".format(o_id,o_name.upper()))
            orgNum = int(input())

            return dbHandlerObj.addEmpToDb(name.lower(), self.email.lower(), pass_, orgNum), self.email

    def loginEmployee(self, dbHandlerObj: DbHandler):
        email = input("Enter you email: ")
        response = dbHandlerObj.checkEmpinDb(email)
        if response:
            pass_ = input("Enter the password: ")
            if pass_ == dbHandlerObj.getPassword(email):
                return 1, email
            else: return -1, None
        else: return 0, None


class Admin(Employee):
    def checkAdmins(self, emp_email, dbHandlerObj:DbHandler):
        response = dbHandlerObj.checkAdminsInDB(emp_email)
        if response == 1:
            Decorator().message("You are the first employee from your ORGANISATION to get registered. Therefore, assigning you as the SUPER ADMIN")