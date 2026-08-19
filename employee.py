from dbHandler import DbHandler
import printStatements as ps

class Employee:
    
    def registerEmployee(self, dbHandlerObj: DbHandler):
        self.email = input(ps.empRegEmail)
        response = dbHandlerObj.checkEmpinDb(self.email)
        if response:
            print(ps.empPresent)
        else:
            name = input(ps.empRegName)
            pass_ = input(ps.empRegPassword)
            cursor = dbHandlerObj.getOrg()
            print("To Which Organisation You Belong To ?")
            for o_id, o_name in cursor:
                print("Click {} for {}".format(o_id,o_name.upper()))
            orgNum = int(input())

            return dbHandlerObj.addEmpToDb(name.lower(), self.email.lower(), pass_, orgNum)


