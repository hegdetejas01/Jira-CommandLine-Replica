from decorator import Decorator
import printStatements as ps
from organisation import Organisation
from dbHandler import DbHandler
from employee import Employee
from employee import Admin

print()

class MainProgram:

    def __init__(self):
        self.dbObj = DbHandler()
        self.empObj = Employee()
        self.orgObj = Organisation()
        self.decoratorObj = Decorator()
        self.admObj = Admin()

        if self.dbObj.conn == None:
            print(ps.dbConnectionFailure)
            exit()

        self.decoratorObj.message(ps.welcomeMessage)
        self.__firstInput()

    def __firstInput(self):

        input1 = int(input(ps.input1))

        if input1 == 1: 
            self.__loginInput()
        elif input1 == 2: 
            self.__registerInput()
        else: pass

    def __loginInput(self):
        loginInput = int(input(ps.loginInput))

        if loginInput == 1: 
            responseNum, responseStr = self.empObj.loginEmployee(dbHandlerObj=self.dbObj)
            if responseNum == 1:
                self.loggedUser = responseStr
                self.decoratorObj.message(ps.empLoginSuccess)

            elif responseNum == 0:
                self.decoratorObj.message(ps.empDoesnotExist)
                self.__registerInput()
            elif responseNum == -1:
                self.decoratorObj.message(ps.empCredMisMatch)
                self.__loginInput()

        elif loginInput == 2: pass
        elif loginInput == 3: 
            self.__firstInput()
        else: pass


    def __registerInput(self):
        registerInput = int(input(ps.registerInput))

        if registerInput == 1: 
            response = self.orgObj.registerOrg(dbHandlerObj=self.dbObj)

            if response == 0:
                print(ps.orgExists)
            elif response == -1:
                print(ps.orgAddFailure)
            elif response == 1:
                self.decoratorObj.message(ps.orgAddSuccess)

        elif registerInput == 2: 
            responseNum, responseEmail = self.empObj.registerEmployee(dbHandlerObj=self.dbObj)

            if responseNum == 0:
                print(ps.empRegFailed)
            elif responseNum == 1:
                print(ps.empRegSuccess)
                self.admObj.checkAdmins(self, responseEmail, dbHandlerObj=self.dbObj)

        elif registerInput == 3: 
            self.__firstInput()
        else: pass


obj = MainProgram()