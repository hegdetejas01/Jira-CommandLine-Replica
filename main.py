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

        input1 = input(ps.input1).strip()

        if input1 == '1': 
            self.__loginInput()
        elif input1 == '2': 
            self.__registerInput()
        else: pass

    def setSession(self, name, userType):
        self.username = name
        self.loggedProfile = userType

    def __loginInput(self):
        loginInput = input(ps.loginInput).strip()

        if loginInput == '1': # employee login
            response = self.empObj.loginEmployee(dbHandlerObj=self.dbObj)
            if response == 1:
                self.LoggedIn = True
            elif response == -1:
                self.__loginInput()
            elif response == 0:
                self.__registerInput()

        elif loginInput == '2': # go back
            self.__firstInput()
            
        else: quit()

    def __registerInput(self):
        registerInput = input(ps.registerInput).strip()

        if registerInput == '1':  # register organisation
            response = self.orgObj.registerOrg(dbHandlerObj=self.dbObj)
            if response == 1:
                self.__loginInput()
            elif response == 0:
                self.__registerInput()

        elif registerInput == '2':  # register employee
            response = self.empObj.registerEmployee(dbHandlerObj=self.dbObj)
            if response == 1: 
                self.__loginInput()
            elif response == 0:
                self.__registerInput()

        elif registerInput == '3': 
            self.__firstInput()

        else: pass

obj = MainProgram()