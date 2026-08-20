from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from organisation import Organisation

class Employee:
    
    def registerEmployee(self, dbHandlerObj: DbHandler):
        self.email = input(ps.empRegEmail)
        response = dbHandlerObj.checkEmpinDb(self.email)
        if response:
            print(ps.empPresent)
        else:
            name = input(ps.empRegName)
            pass_ = input(ps.empRegPassword)

            cursor = Organisation().getOrg(dbHandlerObj)
            print(ps.askOrg)
            for o_id, o_name in cursor:
                print("Click {} for {}".format(o_id,o_name.upper()))
            orgNum = int(input())

            return dbHandlerObj.addEmpToDb(name.lower(), self.email.lower(), pass_, orgNum), self.email

    def loginEmployee(self, dbHandlerObj: DbHandler):
        email = input("Enter you email: ")
        responseDb = dbHandlerObj.checkEmpinDb(email)
        if responseDb is not None: # means employee is in DB

            passInput = input("Enter Your Password: ")
            if responseDb[1] == passInput:
                responseAdm = dbHandlerObj.checkEmpinAdm(responseDb[0])

                self.loggedUser = email # setting the logged user name
                self.loggedProfile = responseAdm # setting who has logged in "S", "A", "E"

                return responseAdm, email
            
            else: 
                return 0, None # incorrect credentials
        else: 
            return -1, None # employee donot exists

class Admin(Employee):
    def checkAdmins(self, emp_email, dbHandlerObj:DbHandler):
        responseAdminCheck = dbHandlerObj.checkAdminsInDB(emp_email)
        if responseAdminCheck == 1:
            Decorator().message("You are the first employee from your ORGANISATION to get registered. Therefore, assigning you as the SUPER ADMIN")
            responseAdmAddCheck = dbHandlerObj.addAdminToDb(emp_email, adminType='S')
            return responseAdmAddCheck
        
        elif responseAdminCheck == 0:
            return 0