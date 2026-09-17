from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from organisation import Organisation
from project import Project


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

    def exitSession(self):
        self.name = None
        self.profile = None
        self.orgId = None
        return 1
    
    def logOut(self):
        name = self.name
        response = self.exitSession()
        if response: print(ps.logoutSuccess.format(name))
        print("\n\n\n")

        from main import MainProgram
        MainProgram()

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
                    orgId = dbHandlerObj.getOrg(caller = 'E', email= email)
                    Decorator().message(ps.adminLoginSuccess.format(email))
                    superAdmEmp = Admin(dbHandlerObj=dbHandlerObj, name=email, profile='S', orgId=orgId)
    
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

    def __init__(self, dbHandlerObj:DbHandler ,name=None, profile=None, orgId=None, caller=None):
        super().__init__(name, profile, orgId)
        if caller != 'S':
            self.displayAdminMenu(dbHandlerObj)

    def logOut(self):
        super().logOut()

    def displayAdminMenu(self, dbhandlerobj : DbHandler):
        admInput = input(ps.AdmMainMenu)

        if admInput == '1':
            self.createProjects(dbhandlerobj, caller='A')

        elif admInput == '2':
            self.editProjects(dbhandlerobj, caller='A')

        elif admInput == '3':
            self.logOut()

    def createProjects(self, dbhandlerobj:DbHandler, caller=None):
        response = Project().createProject(self.orgId, dbhandlerobj)
        if caller == 'S':
            return response

        if response == 1:
            self.displayAdminMenu(dbhandlerobj)
        elif response == 0:
            self.createProjects(dbhandlerobj, caller='A')

    def editProjects(self, dbhandlerobj:DbHandler, caller=None):
        response = Project().editProject(self.orgId, dbhandlerobj)
        if caller == 'S':
            return response

        if response == 1:
            self.displayAdminMenu(dbhandlerobj)
        elif response == 0:
            self.editProjects(dbhandlerobj, caller='A')

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
        super().__init__(name, profile, orgId, caller='S')
        self.displaySuperMenu(dbHandlerObj)

    def displaySuperMenu(self, dbhandlerobj : DbHandler):
        sAdmInput = input(ps.superAdmMainMenu)

        if sAdmInput == '1':
            """
            A company can have a maximum upto 2 Admins
            It is assigned by super admin of the company
            """
            self.assignAdmins(dbhandlerobj)

        elif sAdmInput == '2':
            self.editAdmins(dbhandlerobj)

        elif sAdmInput == '3':
            self.createProjects(dbhandlerobj, caller='S')
                
        elif sAdmInput == '4':
            self.editProjects(dbhandlerobj, caller='S')

        elif sAdmInput == '5':
            super().logOut()

    def createProjects(self, dbhandlerobj, caller=None):
        response = super().createProjects(dbhandlerobj, caller)
        if response == 1:
            self.displaySuperMenu(dbhandlerobj)
        elif response == 0:
            self.createProjects(dbhandlerobj, caller='S')

    def editProjects(self, dbhandlerobj, caller=None):
        response = super().editProjects(dbhandlerobj, caller)
        if response == 1:
            self.displaySuperMenu(dbhandlerobj)
        elif response == 0:
            self.editProjects(dbhandlerobj, caller='S')

    def assignAdmins(self, dbhandlerobj : DbHandler):

        responseAdm = dbhandlerobj.checkAdminsInDB(org_id = self.orgId, caller='S') # gets the number of admin (super admin not included) in the the db for a particular organisation
        responseEmp = dbhandlerobj.checkEmpinDb(org_id = self.orgId, caller='S') # gets the number of employees of the company for the perticular organisation

        if responseEmp - responseAdm - 1 == 0:
            print(ps.insufficientEmpForAdm)
            self.displaySuperMenu(dbhandlerobj)
            
        elif responseAdm == 2:
            i = input(ps.maxAdmLimit)
            if i == '1': self.editAdmins(dbhandlerobj)
            else: 
                print(ps.returnSuperAdmMainMenu)
                self.displaySuperMenu(dbhandlerobj)

        elif responseAdm < 2:

            cursorEmp = dbhandlerobj.getEmployeesEligible(org_id=self.orgId, caller='S')
            manIds = set()
            cursorMan = dbhandlerobj.getManagerList()
            for ids in cursorMan:
                manIds.add(ids[0])

            count = 0
            for data in cursorEmp:
                if data[2] not in ['A', 'S']:
                    if data[0] not in manIds:
                        count += 1

            if count == 0:
                print(ps.empNotAvailableForAdmin)

            else:
                print(ps.empAsAdmin)
                for data in cursorEmp:
                    if data[2] not in ['A', 'S']:
                        if data[0] not in manIds:
                            print(ps.printForAdmSelection.format(data[0], data[1], data[3]))

                chooseAdm = int(input())

                response = dbhandlerobj.addAdms(chooseAdm)
                if response:
                    print(ps.adminSuccessAdd.format(chooseAdm, self.orgId))

            self.displaySuperMenu(dbhandlerobj)

    def editAdmins(self, dbhandlerobj : DbHandler):
        admNum = dbhandlerobj.checkAdminsInDB(org_id=self.orgId, caller='S')
        if admNum == 0: 
            print(ps.noAdmYet)
            self.displaySuperMenu(dbhandlerobj)

        if admNum > 0:
            admIds = []
            adms = dbhandlerobj.getAdm(self.orgId)
            print(ps.admRemoveId)
            for data in adms:
                admIds.append(data[0])
                print(ps.editAdmOp.format(data[0], data[1], data[2]))
            print(ps.exitClick)

            i = input()
            try:
                if int(i) in admIds:
                    response = dbhandlerobj.removeAdm(admId=int(i))
                    if response:
                        print(ps.admRemoveSuccess.format(i))
                    else: print()
                else:
                    print(ps.invalidInput)

            except:
                print(ps.returnSuperAdmMainMenu)

            self.displaySuperMenu(dbhandlerobj)