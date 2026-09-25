from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from organisation import Organisation
from project import Project


class Employee:

    def __init__(self, name=None, profile=None, orgId=None, empId=None):
        self.name = name
        self.profile = profile
        self.orgId = orgId
        self.empId = empId

    def setLoginTime(self, email, dbhandlerobj: DbHandler):
        """
        sets last login timee
        """
        dbhandlerobj.setLoginDateTime(email)

    def exitSession(self):
        self.name = None
        self.profile = None
        self.orgId = None
        self.empId = None
        self.prId = None

        return 1
    
    def logOut(self):
        name = self.name
        response = self.exitSession()
        if response: print(ps.logoutSuccess.format(name))
        print("\n\n\n")

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
                orgId = dbHandlerObj.getOrg(caller = 'E', email= email)
                empId = dbHandlerObj.getEmpId(caller = 'E', email = email)

                if responseAdm == 'S':
                    Decorator().message(ps.superAdmLoginSuccess.format(email))
                    SuperAdmin(dbHandlerObj=dbHandlerObj, name=email, profile='S', orgId=orgId, empId=empId)
    
                elif responseAdm == 'A':
                    Decorator().message(ps.adminLoginSuccess.format(email))
                    Admin(dbHandlerObj=dbHandlerObj, name=email, profile='S', orgId=orgId, empId=empId)
    
                elif responseAdm == 'E':
                    isManager = dbHandlerObj.isManager(email)
                    if isManager:
                        Decorator().message(ps.manLoginSuccess.format(email))
                        Manager(dbHandlerObj=dbHandlerObj, name=email, profile='M', orgId=orgId, empId=empId)
                    else:
                        Decorator().message(ps.empLoginSuccess.format(email))
                        Employee(dbHandlerObj=dbHandlerObj, name=email, profile='E', orgId=orgId, empId=empId)

                return 1
            
            else: # when the credential mismatches
                Decorator().message(ps.empCredMisMatch)
                return -1
        else: # when emp not in DB
            Decorator().message(ps.empDoesnotExist)
            return 0


class Admin(Employee):

    def __init__(self, dbHandlerObj:DbHandler ,name=None, profile=None, orgId=None, empId=None, caller=None):
        super().__init__(name, profile, orgId, empId)
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

    def __init__(self, dbHandlerObj:DbHandler, name, profile, orgId, empId):
        super().__init__(dbHandlerObj, name, profile, orgId, empId, caller='S')
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


class Manager(Employee):

    def __init__(self, dbHandlerObj:DbHandler, name=None, profile=None, orgId=None, empId=None):
        super().__init__(name=name, profile=profile, orgId=orgId, empId=empId)
        self.managerOptions(dbHandlerObj)

    def logOut(self):
        super().logOut()

    def addEmpToProj(self, dbhandlerobj, prId=None):
        """
            # 1. get the projects for which he is the manager
            # 2. get all the employees of this org except the A, S, all those who are already present in that project and self
            # 3. create dropdown to select the employee

            # return 1 to call the same function
            # return 0 to call the manager options
        """

        if prId is None:
            projIds = []
            projData = Project().getProjects(dbhandlerobj, self.empId)

            print(ps.projSelect)
            for project in projData:
                projIds.append(project[0])
                print(ps.projSelectDetail.format(project[0], project[1]))
            prId = int(input())

            if prId not in projIds:
                print(ps.invalidInput)
                self.managerOptions(dbhandlerobj)
                return

        self.prId = prId
        
        empData = dbhandlerobj.getEmployeesEligible(org_id=self.orgId, caller='M')
        empIds = [data[0] for data in empData if data[2] not in {'A', 'S'} and data[0] != self.empId]

        if len(empIds) == 0:
            print(ps.noEmpForPr)
            self.managerOptions(dbhandlerobj)
            return

        print(ps.askEmpAdd)

        for data in empData:
            if data[0] in empIds:
                print(ps.empForPr.format(data[0], data[1], data[3]))

        empSelected = [int(i) for i in input().strip().split()]

        count = 0
        for emp in empSelected:
            if emp not in empIds:
                count += 1
                print(ps.invalidEmpInput, emp)

            else:
                print(ps.addEmpToWork.format(emp))
                response = dbhandlerobj.addEmpToWork(prId = self.prId, empId = emp)
                if response:
                    print(ps.addEmpToWorkSuccess.format(emp))
                else:
                    print(ps.addEmpToWorkFailure.format(emp))

        if count != 0:
            print(ps.manOpsRedirect)

        self.managerOptions(dbhandlerobj)
        return

    def removeEmpFromProj(self, dbhandlerobj, prId = None):
        """
            # drop down menu of the proj for which he is the manager
            # ask him to select th proj
            # check if there are employees in that project 
            # if no, ask him to add employees to the project (send the prID)
            # if yes, drop down menu of empId and name for him to remove
        """

        if prId is None:
            projIds = []
            projData = Project().getProjects(dbhandlerobj, self.empId)

            print(ps.projSelect)
            for project in projData:
                projIds.append(project[0])
                print(ps.projSelectDetail.format(project[0], project[1]))
            prId = int(input())

            if prId not in projIds:
                print(ps.invalidInput)
                self.managerOptions(dbhandlerobj)
                return

        self.prId = prId

        empData = dbhandlerobj.getEmpInProj(prId=self.prId)
        empIds = [data[0] for data in empData if data[2] not in {'A', 'S'} and data[0] != self.empId]

        if len(empIds) == 0:
            print("No Employees are yet present in the project... Try Adding the employees for the project first")
            self.addEmpToProj(dbhandlerobj, self.prId)
            return

        else:
            print("\nWhom do you want to remove? If there are multiple employee keep it space saperated...")
            for emp in empData:
                if emp[0] in empIds:
                    print("Click {} to remove {} ({}) from this project (ID = {})".format(emp[0], emp[2], emp[1], self.prId))
            print(ps.exitClick)

            empToRemove = [int(i) for i in input().strip().split()]

        count = 0
        for emp in empToRemove:
            if emp not in empIds:
                count += 1
                print(ps.invalidEmpInput, emp)

            else:
                print(ps.removeEmpFromWork.format(emp))
                response = dbhandlerobj.removeEmpFromWork(prId = self.prId, empId = emp)
                empIds.remove(emp)

                if response:
                    print(ps.removeEmpFromWorkSuccess.format(emp))
                else:
                    print(ps.removeEmpFromWorkFailure.format(emp))

        if count != 0:
            print(ps.manOpsRedirect)

        self.managerOptions(dbhandlerobj)
        return

    def managerOptions(self, dbhandlerobj : DbHandler):
        manInput = input(ps.manMainMenu)

        if manInput == '1':
            self.addEmpToProj(dbhandlerobj)
    
        elif manInput == '2':
            self.removeEmpFromProj(dbhandlerobj)

        elif manInput == '3':
            # create ticket
            pass
        elif manInput == '4':
            # edit ticket
            pass
        elif manInput == '5':
            self.logOut()