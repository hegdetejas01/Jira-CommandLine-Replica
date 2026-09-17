from decorator import Decorator
from dbHandler import DbHandler
import printStatements as ps

class Project:

    def empOtherThanAandS(self, orgId, dbhandlerobj, caller=None):

        empData = dbhandlerobj.getEmployeesEligible(org_id=orgId, caller='P')

        empIds = []
        for data in empData:
            if data[2] != 'S' and data[2] != 'A':
                empIds.append(data[0])

        if (caller == 'create' and len(empIds) == 0) or (caller == 'edit' and len(empIds) == 1): 
            return 1, empIds, empData

        else: return 0, empIds, empData


    def createProject(self, orgId, dbhandlerobj: DbHandler):
        proName = input(ps.proName)
        print(ps.manId)

        response, empIds, empData = self.empOtherThanAandS(orgId, dbhandlerobj)
        if response == 1: 
            print(ps.noManForPro)
            return 1 # call main menu

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

    def editProject(self, orgId, dbhandlerobj:DbHandler):
        """
        Project will be fetched based on the organistion id of the logged admin or super admin
        Admin or Super Admin can change the name of the project and the managers assigned to the project
        """
        self.orgId = orgId

        projects = dbhandlerobj.getProjectList(orgId)
        prId = []

        if projects is not None:
            print(ps.askEditProj)
            for project in projects:
                prId.append(project[0])
                print(ps.projEditNum.format(project[0],  project[1].upper()))
            edit = int(input())

            if edit not in prId:
                print(ps.invalidInput)
                # get the main menu based on caller
                return 0

            else:

                newProjName = None
                newManId = None

                self.prId = edit
                for project in projects:
                    if project[0] == edit:
                        self.manId = project[3]

                        nameEdit = input(ps.askProjNameEdit.format(project[1].upper()))

                        if nameEdit == 'y' or nameEdit == 'Y':
                            newProjName = input(ps.askProjNewName)
                        else: newProjName = None

                        managerEdit = input(ps.askManNameEdit.format(project[2].upper()))

                        if managerEdit == 'y' or managerEdit == 'Y':
                            response, empIds, empData = self.empOtherThanAandS(orgId, dbhandlerobj)
                            if response == 1:
                                print(ps.manNotAvailable)
                                return 1 # call main menu

                            else:
                                for data in empData:
                                    if data[2] != 'S' and data[2] != 'A':
                                        print(ps.newManToPro.format(data[0], data[1], data[3]))
                                print(ps.exitClick)
                                i = int(input())

                                if i in empIds:
                                    newManId = i

                                else: 
                                    print(ps.invalidInput)
                                    return 0 # call edit function
                                
                        else:
                            newManId = None

                        response = dbhandlerobj.editProjectInDb(prId=self.prId, newProjName=newProjName, newManId=newManId)
                        if response == 1:
                            print(ps.projEditSuccess)
                            return response
                        # 1 if addition is successfull - call main menu
                        # 0 if not edited in db - call edit function

                        else:
                            print(ps.projEditFailed)
                            return 0 # call edit funtion