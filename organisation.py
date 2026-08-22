import printStatements as ps
from dbHandler import DbHandler
from decorator import Decorator

class Organisation:

    def registerOrg(self, dbHandlerObj: DbHandler):
        """
        Returns 1 for loginpage
        Returns 0 for registerpage
        """
        name = input(ps.getOrgName)
        response  =  dbHandlerObj.addOrgToDb(name.strip().lower())
        if response == 0:
            print(ps.orgExists)
            return 1
        elif response == -1:
            print(ps.orgAddFailure)
            return 0
        elif response == 1:
            Decorator().message(ps.orgAddSuccess)
            return 1

    def getOrg(self, dbHandlerObj: DbHandler):
        return dbHandlerObj.getOrg()