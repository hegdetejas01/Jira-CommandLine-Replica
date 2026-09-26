from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from project import Project
import datetime as dt

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
            print(ps.clickForThis.format(DbData[0], DbData[1]))
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
        title = input(ps.askTitle)
        if len(title) == 0:
            print(ps.titleEmpty)
            return 0
        
        self.title = title
        return 1      

    def changeAssignee(self, dbhandlerobj):
        projEmpData = dbhandlerobj.getEmpInProj(prId=self.prId)
        if len(projEmpData) == 1:
            return -1

        empIds = []
        print(ps.askAssignee)
        for emp in projEmpData:
            if emp[0] != self.empId:
                empIds.append(emp[0])
                print(ps.selectAssignee.format(emp[0], emp[2], emp[1]))
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
        desc = input(ps.askDesc)
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
            print(ps.invalidStatus)
            self.status = dbhandlerobj.getIndiviadualStatus(status='TO DO')

        if self.status == dbhandlerobj.getIndiviadualStatus(status='DONE'):
            self.resolvedDate = 1 # while adding to db check if this is 1, then add the current date time, else leve it as it is...
        else: self.resolvedDate = None

#  assignee for the ticket
        changeAssignee = input(ps.askChangeAssignee)
        changeAssignee = changeAssignee.lower()

        if changeAssignee == 'y':
            response = self.changeAssignee(dbhandlerobj)

            if response == -1:
                print(ps.noEmpForAssignee)
                self.assignee = empId

            elif response == 0:
                print(ps.defaultAssignee)
                self.assignee = empId
                
            elif response == 1:
                print(ps.assigneeChangeSuccess)
            
        elif changeAssignee == 'n':
            print(ps.selfAssignee)
            self.assignee = empId
            
        else:
            print(ps.defaultAssignee)
            self.assignee = empId

# ticketId for the ticket
        self.generateTicketId(dbhandlerobj)

# create a entry in the database
        response = self.pushDetailsToDb(dbhandlerobj)
        return response

    def pushDetailsToDb(self, dbhandlerobj):
        response = dbhandlerobj.createTicketInDb(self.ticketId, self.prId, self.title, self.type, self.createdBy, self.assignee, self.priority, self.status, self.resolvedDate, self.desc)
            
        if response:
            Decorator().message(ps.ticketSuccess)
            return 1
        else:
            Decorator().message(ps.ticketFailure)
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

    def viewTicket(self, prId, dbhandlerobj:DbHandler):
        # fetch all the tickets of that project
        # drop down menu
        # display

        # return 1 for main menu
        # return 0 for the same function
        # return -1 for create ticket function

        allTickets = dbhandlerobj.getAllTickets(prId=prId)
        if len(allTickets) == 0:
            y = input(ps.noTicket)
            if y.lower() == 'y':
                return -1 # call create ticket
            else:
                return 1 # call main menu

        ticketIds = []
        print(ps.viewTicket)
        for ticket in allTickets:
            ticketIds.append(ticket[0])
            desc = f"{ticket[2][:20]}..." if ticket[2] is not None else ps.noDesc
            print(ps.selectTicketDisplay.format(ticket[0], ticket[1], desc))
        userInput = input()

        try:
            userInput = int(userInput)
        except:
            print(ps.invalidInput)
            return 0

        if userInput not in ticketIds:
            print(ps.invalidInput)
            return 0

        self.ticketId = userInput

        response = dbhandlerobj.getTicketDetails(ticketId=self.ticketId)
        if response is None:
            print(ps.uunexpected)
            return 0

        else:
            self.ticketDisplay(data=response[0])
            return 1

    def ticketDisplay(self, data):
        mainMessage = ps.mainDisplay.format(data[2], data[0], data[1])
        Decorator().message(mainMessage)

        if data[6] is not None:
            print(f"Description - {data[6].title()}")
        else:
            print(ps.noDesc)

        print(ps.tpsDisplay.format(data[3], data[4], data[5]))
        print(ps.acDisplay.format(data[7], data[8]))

        createdDate = data[9].strftime("%d %b %Y, %I:%M %p")
        modifiedDate = data[10].strftime("%d %b %Y, %I:%M %p")
        print(ps.dateDisplay.format(createdDate, modifiedDate))

        if data[11] is not None:
            resolvedDate = data[11].strftime("%d %b %Y, %I:%M %p")
            print(ps.resDate.format(resolvedDate))