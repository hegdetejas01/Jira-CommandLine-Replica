from decorator import Decorator
from dbHandler import DbHandler
import printStatements as ps

class Project:

    def __init__(self, prName=None, managerId=None):
        self.prName = prName
        self.manager = managerId

    def createProject(self, orgid, dbhandlerobj: DbHandler):
        proName = input(ps.proName)
        print(ps.manId)
        empData = dbhandlerobj.getEmployeesEligible(org_id=orgid, caller='P')

        empIds = []
        for data in empData:
            if data[2] != 'S' and data[2] != 'A':
                empIds.append(data[0])

        if len(empIds) == 0: 
            print(ps.noManForPro)
            return 1
        
        for data in empData:
            if data[2] != 'S' and data[2] != 'A':
                print(ps.manToPro.format(data[0], data[1], data[3]))

        print(ps.exitClick)
        i = input()

        try:
            if int(i) in empIds:
                response = dbhandlerobj.createProjectinDb(proName, int(i))
                if response: 
                    print(ps.proSuccessToDb) 
                    # return 1 # call mainmenu
                    return 1
                else: 
                    print(ps.proFailedToDb) 
                    # return 0 # again call create project
                    return 0

            else:
                print(ps.invalidInput)
                # return -1 # call createproject
                return 0

        except:
            # return 'x' # call mainmenu
            print(ps.returnSuperAdmMainMenu)
            return 1

    def editProject(self, dbhandlerobj:DbHandler):
        pass