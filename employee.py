from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from organisation import Organisation

class Employee:

    def setSession(self, name, profile, dbhandlerobj: DbHandler):
        """
        sets username and profile for the logged user
        """
        self.name = name
        self.profile = profile
        dbhandlerobj.setLoginDateTime(name)

    def logoutEmployee(self):
        """
        Returns 1 after logging out
        """
        self.name = None
        self.profile = None
        return 1

    def exitSession(self):
        self.name = None
        self.profile = None
        return 1
    
    def loggedInOptions(self):
        userInput = input("Click 1 to logout").strip()
        if userInput == '1': 
            name = self.name
            response = self.exitSession()
            if response: print(ps.logoutSuccess.format(name))

    def registerEmployee(self, dbHandlerObj: DbHandler):
        """
        Input: DB handler object
        Output:
            1 : if employee is already present - login page
            1 : employee added successfully - login page
            0 : employee not in db, but registration failed - registration page
        """
        email = input(ps.empRegEmail)
        response = dbHandlerObj.checkEmpinDb(email)
        if response: # employee already present
            print(ps.empPresent)
            return 1
        else:
            name = input(ps.empRegName)
            pass_ = input(ps.empRegPassword)

            cursor = Organisation().getOrg(dbHandlerObj)
            print(ps.askOrg)
            for o_id, o_name in cursor:
                print("Click {} for {}".format(o_id,o_name.upper()))
            orgNum = int(input())

            response =  dbHandlerObj.addEmpToDb(name.lower(), email.lower(), pass_, orgNum)

            if response == 1:
                print(ps.empRegSuccess)
                responseAddAdmin = Admin().checkAdmins(email, dbHandlerObj)
                if responseAddAdmin == 1: 
                    Decorator().message(ps.superAdmRegisterSuccess)

                return 1
            
            elif response == 0:
                print(ps.empRegFailed)
                return 0

    def loginEmployee(self, dbHandlerObj: DbHandler):
        """
        Input: a db handler object
        Output:
            Return 1 : For Successfull Login
            Return 0 : If Employee Not present in DB - call register page
            Return -1 : For credentials mismatch - call login page
        """
        email = input("Enter you email: ")
        responseDb = dbHandlerObj.checkEmpinDb(email)
        if responseDb is not None: # means employee is in DB

            passInput = input("Enter Your Password: ")
            if responseDb[1] == passInput:
                responseAdm = dbHandlerObj.checkEmpinAdm(responseDb[0]) # gets S E or A

                self.setSession(email, responseAdm, dbHandlerObj)

                if responseAdm == 'S':
                    Decorator().message(ps.superAdmLoginSuccess.format(email))
    
                elif responseAdm == 'A':
                    Decorator().message(ps.adminLoginSuccess.format(email))
    
                elif responseAdm == 'E':
                    Decorator().message(ps.empLoginSuccess.format(email))

                self.loggedInOptions()

                return 1
            
            else: # when the credential mismatches
                Decorator().message(ps.empCredMisMatch)
                return -1
        else: # when emp not in DB
            Decorator().message(ps.empDoesnotExist)
            return 0

class Admin(Employee):
    def checkAdmins(self, emp_email, dbHandlerObj:DbHandler):
        """
        Returns 1 if the employee is added as super Admin, else 0
        """
        responseAdminCheck = dbHandlerObj.checkAdminsInDB(emp_email)
        if responseAdminCheck == 1:
            Decorator().message(ps.superAdminAssigned)
            responseAdmAdd = dbHandlerObj.addAdminToDb(emp_email, adminType='S')
            return responseAdmAdd
        
        elif responseAdminCheck == 0:
            return 0

class SuperAdmin(Admin):
    pass