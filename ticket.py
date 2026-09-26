from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from project import Project

"""
create table ticket( 
    id INTEGER AUTO_INCREMENT UNIQUE,                       - autoassigned
    ticket_id VARCHAR(255) PRIMARY KEY,                     - to be done by developer
    pr_id INTEGER NOT NULL,                                 - drop down
    title VARCHAR(255) NOT NULL,                            - user
    description TEXT NOT NULL,                              - user
    ticket_type INT NOT NULL,                               - drop down
    created_by INT NOT NULL,                                - auto assigned
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,   - autoassigned
    modified_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,  - autoassigned
    resolved_date DATETIME,                                     - autoassigned
    assignee INT NOT NULL,                                      - autoassigned (but can be changed)
    priority INT NOT NULL,                                      - drop down
    due_date DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 3 DAY) NOT NULL,    - autoassigned
    ticket_status INT NOT NULL,                                                 - drop down
)

"""

class Ticket:

    def getSuppDetails(self,  dbhandlerobj, what=None):
        printDict = {
            'priority':'\nWhat is the priority of the ticket',
            'type':'\nWhat type of ticket you want to create...',
            'status':'\nWhat is the status of the ticket'
        }

        print(printDict[what])
        DbDatas = dbhandlerobj.getSuppTicketData(what=what)

        datas = []
        for DbData in DbDatas:
            datas.append(DbData[0])
            print("Click {} to select {}".format(DbData[0], DbData[1]))
        userInput = input()

        try:
            userInput = int(userInput)
        except:
            if what != 'status':
                print(ps.invalidInput)
            return 0

        if userInput not in datas:
            if what != 'status':
                print(ps.invalidInput)
            return 0

        if what == 'priority': self.priority=userInput
        elif what == 'status': self.status=userInput
        elif what == 'type':self.type=userInput
        return 1

    def getTitle(self):
        title = input("Enter the Title: ")
        if len(title) == 0:
            print("Title can't be empty... Try Again")
            return 0
        
        self.title = title
        return 1      

    def changeAssignee(self, dbhandlerobj):
        projEmpData = dbhandlerobj.getEmpInProj(prId=self.prId)
        if len(projEmpData) == 1:
            return -1

        empIds = []
        print("Whom do you want to select as assignee??...")
        for emp in projEmpData:
            if emp[0] != self.empId:
                empIds.append(emp[0])
                print("Click {} to select {} ({}) as assignee to this ticket".format(emp[0], emp[2], emp[1]))
        userInput = input()

        try:
            userInput = int(userInput)
        except: 
            return 0

        if userInput not in empIds:
            return 0

        self.assignee = userInput
        return 1

    def createTicket(self, empId, prId, dbhandlerobj: DbHandler):

        # return 0 to call the create ticket function
        # return 1 to call menu

        self.empId = empId
        self.prId = prId
        self.createdBy = empId

#  type of ticket
        response = self.getSuppDetails(dbhandlerobj, what='type')
        if response == 0:
            return 0

#  title for the ticket
        response = self.getTitle()
        if response==0:
            return 0

#  description for the ticket
        desc = input("Enter the Description: ")
        if len(desc) == 0:
            desc = None
        self.desc = desc

#  priority for the ticket
        response = self.getSuppDetails(dbhandlerobj, what='priority')
        if response == 0:
            return 0
        
#  status for the ticket
        response = self.getSuppDetails(dbhandlerobj, what='status')
        if response == 0:
            print("Invalid Input... Assigning the default status - TO DO")
            self.status = dbhandlerobj.getIndiviadualStatus(status='TO DO')

        if self.status == dbhandlerobj.getIndiviadualStatus(status='DONE'):
            self.resolvedDate = 1 # while adding to db check if this is 1, then add the current date time, else leve it as it is...
        else: self.resolvedDate = None

#  assignee for the ticket
        changeAssignee = input("You are the default assignee... Do you want to change the assignee? (y/n)").lower()

        if changeAssignee == 'y':
            response = self.changeAssignee(dbhandlerobj)

            if response == -1:
                print("No other employee is working on this project. Try adding first... You are assigned as the assignee")
                self.assignee = empId

            elif response == 0:
                print("\nInvalid Input... You will be default assignee. You can edit it later")
                self.assignee = empId
                
            elif response == 1:
                print("Successfully changed the assignee")
            
        elif changeAssignee == 'n':
            print("You have selected yourself as the assignee")
            self.assignee = empId
            
        else:
            print("\nInvalid Input... You will be default assignee. You can edit it later")
            self.assignee = empId

# ticketId for the ticket
        self.generateTicketId(dbhandlerobj)

# create a entry in the database
        response = self.pushDetailsToDb(dbhandlerobj)
        return response

    def pushDetailsToDb(self, dbhandlerobj):
        response = dbhandlerobj.createTicketInDb(self.ticketId, self.prId, self.title, self.type, self.createdBy, self.assignee, self.priority, self.status, self.resolvedDate, self.desc)
            
        if response:
            Decorator().message("Ticket Successfully Created")
            return 1
        else:
            Decorator().message("Failed to create the ticket, Try again")
            return 0

    def generateTicketId(self, dbhandlerobj):
        prName = dbhandlerobj.getProjName(prId=self.prId)
        prName = prName.replace(" ", "")

        if len(prName) >= 4:
            nameID = prName[:4]
        else: nameID = prName

        lastId = dbhandlerobj.getLastTicketId(prId=self.prId)
        if lastId is not None:
            num = lastId[0]
            numId = f"{num:04d}"
        else:
            numId = "0000"

        ticketId = nameID+numId
        self.ticketId = ticketId
        

    def updateTicket():
        pass

    def closeTicket():
        pass

    def viewTicket():
        pass