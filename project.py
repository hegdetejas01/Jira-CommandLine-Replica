from decorator import Decorator
from dbHandler import DbHandler

class Project:

    def __init__(self, prName=None, managerId=None):
        self.prName = prName
        self.manager = managerId

    def createProject(self, orgid, dbhandlerobj: DbHandler):
        proName = input("Enter the project name to create: ")
        print("Who is the manager? ")
        empData = dbhandlerobj.getEmployeesEligible(org_id=orgid, caller='P')

        empIds = []
        for data in empData:
            if data[2] not in ['A','S']:
                empIds.append(data[0])
                print("Click {} to assign {} ({}) as manager to the project".format(data[0], data[1], data[3]))

        print("Click x or X to exit...")
        i = input()
        if int(i) in empIds:
            response = dbhandlerobj.createProjectinDb(proName, int(i))
            if response: 
                print("Project Successfully Added to DB...") 
                # return 1 # call mainmenu
                return 1
            else: 
                print("Failed to add project to DB... Try Again...") 
                # return 0 # again call create project
                return 0

        elif i in ['X','x']:
            # return 'x' # call mainmenu
            print("Returning to main menu...")
            return 1

        else:
            print("Invalid Input. Try Again... ")
            # return -1 # call createproject
            return 0

    def editProject(self, dbhandlerobj:DbHandler):
        pass