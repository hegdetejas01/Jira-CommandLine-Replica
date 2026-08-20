import printStatements as ps
from dbHandler import DbHandler

class Organisation:

    def registerOrg(self, dbHandlerObj: DbHandler):
        name = input(ps.getOrgName)
        return dbHandlerObj.addOrgToDb(name.strip().lower())

    def getOrg(self, dbHandlerObj: DbHandler):
        return dbHandlerObj.getOrg()