from decorator import Decorator
import printStatements as ps
from organisation import Organisation
from dbHandler import DbHandler

print()

class MainProgram:

    def __init__(self):
        self.dbObj = DbHandler()
        if self.dbObj.conn == None:
            print(ps.dbConnectionFailure)
            exit()

        decoratorObj = Decorator()
        decoratorObj.message(ps.welcomeMessage)
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

        if loginInput == 1: pass
        elif loginInput == 2: pass
        elif loginInput == 3: 
            self.__firstInput()
        else: pass


    def __registerInput(self):
        registerInput = int(input(ps.registerInput))

        if registerInput == 1: 
            orgObj = Organisation()
            response = orgObj.registerOrg(dbHandlerObj=self.dbObj)

            if response == 0:
                print(ps.orgExists)
            elif response == -1:
                print(ps.orgAddFailure)
            elif response == 1:
                print(ps.orgAddSuccess)

        elif registerInput == 2: pass
        elif registerInput == 3: 
            self.__firstInput()
        else: pass


obj = MainProgram()