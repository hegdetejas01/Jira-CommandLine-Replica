from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from organisation import Organisation

class Employee:

    def __init__(self, name=None, profile=None, orgId=None):
        self.name = name
        self.profile = profile
        self.orgId = orgId

    def setLoginTime(self, email, dbhandlerobj: DbHandler):
        """
        sets last login timee
        """
        dbhandlerobj.setLoginDateTime(email)

    def logoutEmployee(self):
        """
        Returns 1 after logging out
        """
        self.name = None
        self.profile = None
        self.orgId = None
        return 1

    def exitSession(self):
        self.name = None
        self.profile = None
        self.orgId = None
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
        response = dbHandlerObj.checkEmpinDb(email=email)
        if response: # employee already present
            print(ps.empPresent)
            return 1
        else:
            name = input(ps.empRegName)
            pass_ = input(ps.empPassword)

            cursor = Organisation().getOrg(dbHandlerObj)
            print(ps.askOrg)
            for o_id, o_name in cursor:
                print(ps.printOrg.format(o_id,o_name.upper()))
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
        email = input(ps.empLoginEmail)
        responseDb = dbHandlerObj.checkEmpinDb(email=email)
        if responseDb is not None: # means employee is in DB

            passInput = input(ps.empPassword)
            if responseDb[1] == passInput:
                responseAdm = dbHandlerObj.checkEmpinAdm(responseDb[0]) # gets S E or A

                self.setLoginTime(email, dbHandlerObj)

                if responseAdm == 'S':
                    orgId = dbHandlerObj.getOrg(caller = 'E', email= email)
                    Decorator().message(ps.superAdmLoginSuccess.format(email))
                    superAdmEmp = SuperAdmin(dbHandlerObj=dbHandlerObj, name=email, profile='S', orgId=orgId)
    
                elif responseAdm == 'A':
                    Decorator().message(ps.adminLoginSuccess.format(email))
    
                elif responseAdm == 'E':
                    Decorator().message(ps.empLoginSuccess.format(email))

                return 1
            
            else: # when the credential mismatches
                Decorator().message(ps.empCredMisMatch)
                return -1
        else: # when emp not in DB
            Decorator().message(ps.empDoesnotExist)
            return 0

class Admin(Employee):

    def __init__(self, name=None, profile=None, orgId=None):
        super().__init__(name, profile, orgId)

    def createProjects(self):
        pass

    def editProjects(self):
        pass

    def checkAdmins(self, emp_email, dbHandlerObj:DbHandler):
        """
        Returns 1 if the employee is added as super Admin, else 0
        """
        responseAdminCheck = dbHandlerObj.checkAdminsInDB(email=emp_email)
        if responseAdminCheck == 1:
            Decorator().message(ps.superAdminAssigned)
            responseAdmAdd = dbHandlerObj.addAdminToDb(emp_email, adminType='S')
            return responseAdmAdd
        
        elif responseAdminCheck == 0:
            return 0

class SuperAdmin(Admin):

    def __init__(self, dbHandlerObj:DbHandler, name=None, profile=None, orgId=None):
        super().__init__(name, profile, orgId)
        self.displayMenu(dbHandlerObj)

    def assignAdmins(self, dbhandlerobj : DbHandler):
        cursor = dbhandlerobj.getEmployeesEligibleAdmin(org_id = self.orgId)
        print(ps.empAsAdmin)
        for data in cursor:
            if data[2] not in ['A', 'S']:
                print(ps.printForAdmSelection.format(data[0], data[1]))

        chooseAdm = int(input())

        response = dbhandlerobj.addAdms(chooseAdm)
        if response:
            print(ps.adminSuccessAdd.format(chooseAdm, self.orgId))

    def editAdmins(self):
        pass

    def displayMenu(self, dbhandlerobj : DbHandler):
        sAdmInput = input(ps.superAdmMainMenu)

        if sAdmInput == '1':
            """
            A company can have a maximum upto 2 Admins
            It is assigned by super admin of the company
            """
            responseAdm = dbhandlerobj.checkAdminsInDB(org_id = self.orgId, caller='S') # gets the number of admin in the the db for a particular organisation
            responseEmp = dbhandlerobj.checkEmpinDb(org_id = self.orgId, caller='S') # gets the number of employees of the company for the perticular organisation

            if responseAdm == 2:
                if responseEmp - responseAdm - 1 == 0:
                    print(ps.insufficientEmpForAdm)
                    self.displayMenu(dbhandlerobj)
                else:
                    i = input(ps.maxAdmLimit)
                    if i == '1': self.editAdmins()
                    else: 
                        print(ps.returnSuperAdmMainMenu)
                        self.displayMenu(dbhandlerobj)

            elif responseAdm < 2:
                self.assignAdmins(dbhandlerobj)
                self.displayMenu(dbhandlerobj)

        elif sAdmInput == '2':
            # code to edit addmins
            pass

        elif sAdmInput == '3':
            super().createProjects()
            # code to create project - call the method present in admin (inheritance)

        elif sAdmInput == '4':
            super().editProjects()
            # code to edit the info of the project

        elif sAdmInput == '5':
            self.logoutEmployee()