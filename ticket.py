from dbHandler import DbHandler
import printStatements as ps
from decorator import Decorator
from project import Project
import datetime as dt

class Ticket:

    def __init__(self):
        self.ticketId = None
        self.type = None
        self.status = None
        self.priority = None
        self.prId = None
        self.empId = None
        self.resolvedDate = None
        self.createdBy = None
        self.desc = None
        self.title = None
        self.days = None
        self.assignee = None

    def getSuppDetails(self, dbhandlerobj:DbHandler, what=None, caller=None):
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
            if what != 'status' and caller != 'edit':
                print(ps.invalidInput)
            return 0

        if userInput not in datas:
            if what != 'status' and caller != 'edit':
                print(ps.invalidInput)
            return 0

        if what == 'priority': self.priority=userInput
        elif what == 'status': self.status=userInput
        elif what == 'type': self.type=userInput
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
                Decorator().message(ps.assigneeChangeSuccess)
            
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

    def pushDetailsToDb(self, dbhandlerobj:DbHandler):
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

        lastId = dbhandlerobj.getLastTicketId()
        if lastId is not None:
            num = lastId[0]+1
            numId = f"{num:04d}"
        else:
            numId = "0001"

        ticketId = nameID+numId
        self.ticketId = ticketId
        
    def getTicketDeatils(self, prId, caller, dbhandlerobj:DbHandler):
        allTickets = dbhandlerobj.getAllTickets(prId=prId)
        if len(allTickets) == 0:
            y = input(ps.noTicket)
            if y.lower() == 'y':
                return -1 # call create ticket
            else:
                return 1 # call main menu

        ticketIds = []

        if caller == 'edit':
            print(ps.editTicket)
        elif caller  == 'view':
            print(ps.viewTicket)
        elif caller == 'close':
            print(ps.askClose)

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

        if caller == 'edit':
            print(ps.noteToEdit)

        response = dbhandlerobj.getTicketDetails(ticketId=self.ticketId)
        if response is None:
            print(ps.unexpected)
            return 0

        else:
            if caller == 'view':
                response = self.ticketDisplay(data=response[0])

            elif caller == 'edit':
                response = self.editTicket(data=response[0], dbhandlerobj=dbhandlerobj)

            elif caller == 'close':
                response = self.changeStatus(data=response[0], dbhandlerobj=dbhandlerobj)

            return response

    def editTicket(self, data, dbhandlerobj:DbHandler):

        finalResponse = [1,1,1,1,1,1]
        userInputs = []
        nullifyResolvedDate = False
        addResolvedDate = False

        mainMessage = ps.mainDisplay.format(data[2], data[0], data[1])
        Decorator().message(mainMessage)

        self.ticketId = data[0]
        self.oldTicketStatus = dbhandlerobj.getIndiviadualStatus(status=data[5])
        respDesc = respStatus = respAssignee = respType = respPrio = respDue = -1

        userinput = input(ps.editDesc)
        userInputs.append(userinput)
        if userinput.lower() == 'y':
            newDesc = input(ps.askNewDesc)
            if len(newDesc) == 0:
                newDesc = None
            self.desc = newDesc
            respDesc = dbhandlerobj.editTicket(self.ticketId, self.desc, what='desc')
            finalResponse[0] = respDesc

        userinput = input(ps.ticketType)
        userInputs.append(userinput)
        if userinput.lower() == 'y':
            self.type = data[3]
            response = self.getSuppDetails(dbhandlerobj, what='type', caller='edit')
            if response == 0:
                print(ps.invalidInput)
                return 0 # call the same function again
            else: 
                respType = dbhandlerobj.editTicket(self.ticketId, self.type, what='type')
                finalResponse[1] = respType

        userinput = input(ps.editAssignee)
        userInputs.append(userinput)
        if userinput.lower() == 'y':
            oldAssignee = dbhandlerobj.getEmpId(caller='T', email=data[7])
            response = self.changeAssignee(dbhandlerobj)

            if response == -1:
                print(ps.noAssigneeChange)
                self.assignee = oldAssignee

            elif response == 0:
                print(ps.invalidAssignee)
                self.assignee = oldAssignee
                
            elif response == 1:
                Decorator().message(ps.assigneeChangeSuccess)

            respAssignee = dbhandlerobj.editTicket(self.ticketId, self.assignee, what='assignee')
            finalResponse[2] = respAssignee

        userinput = input(ps.editPriority)
        userInputs.append(userinput)
        if userinput.lower() == 'y':
            response = self.getSuppDetails(dbhandlerobj, what='priority',caller='edit')
            if response == 0:
                print(ps.invalidInput)
                return 0 # call the same function again
            else: 
                respPrio = dbhandlerobj.editTicket(self.ticketId, self.priority, what='priority')
                finalResponse[3]= respPrio

        userinput = input(ps.editStatus)
        userInputs.append(userinput)
        if userinput.lower() == 'y':
            response = self.getSuppDetails(dbhandlerobj, what='status', caller='edit')
            if response == 0:
                print(ps.invalidInput)
                return 0 # call the same function again
            else: 
                respStatus = dbhandlerobj.editTicket(self.ticketId, self.status, what='status')
                finalResponse[4] = respStatus
                if respStatus == 1:
                    if self.oldTicketStatus == dbhandlerobj.getIndiviadualStatus('DONE') and self.status != dbhandlerobj.getIndiviadualStatus('DONE'):
                        nullifyResolvedDate = True
                    elif self.oldTicketStatus != dbhandlerobj.getIndiviadualStatus('DONE') and self.status == dbhandlerobj.getIndiviadualStatus('DONE') :
                        addResolvedDate = True

        userinput = input(ps.editDueDate)
        userInputs.append(userinput)
        if userinput.lower() == 'y':
            days = input(ps.askDays)
            try:
                self.days = int(days)
                respDue = dbhandlerobj.editTicket(self.ticketId, days, what='due')
                finalResponse[5] = respDue
            except:
                Decorator().message(ps.editDueDateFailure)

        userChoice = set(userInputs) != {'n'}

        if userChoice:
            proceed = set(finalResponse) == {1}
            if proceed:
                if self.days is not None: respDue = dbhandlerobj.editTicket(self.ticketId, self.days, what='due', why='update')
                dbhandlerobj.changeDate(self.ticketId, which='m')

                if self.status is not None: respStatus = dbhandlerobj.editTicket(self.ticketId, self.status, what='status', why='update')
                if nullifyResolvedDate:
                    dbhandlerobj.changeDate(self.ticketId, which='r', what='null')
                if addResolvedDate:
                    dbhandlerobj.changeDate(self.ticketId, which='r', what='add')

                if self.priority is not None: respPrio = dbhandlerobj.editTicket(self.ticketId, self.priority, what='priority', why='update')
                if self.assignee is not None: respAssignee = dbhandlerobj.editTicket(self.ticketId, self.assignee, what='assignee', why='update')
                if self.type is not None: respType = dbhandlerobj.editTicket(self.ticketId, self.type, what='type', why='update')
                if self.desc is not None: respDesc = dbhandlerobj.editTicket(self.ticketId, self.desc, what='desc', why='update')

                print()
                Decorator().message(ps.ticketEditSuccess)
                return 1 # call main menu
            
            else:

                if respType == 0: messageSub = "'TICKET TYPE'"
                elif respAssignee == 0: messageSub = "'ASSIGNEE'"
                elif respDesc == 0: messageSub = "'DESCRIPTION'"
                elif respDue == 0: messageSub = "'DUE DATE'"
                elif respPrio == 0: messageSub = "'TICKET PRIORITY'"
                elif respStatus == 0: messageSub = "'TICKET STATUS'"
                else: messageSub = ps.unknownError

                finalMessage = ps.messageMain + messageSub

                Decorator().message(finalMessage)
                return 0 # call the same function

        else:
            Decorator().message(ps.noEditDone)
            return 0

    def updateTicket(self, empId, prId, dbhandlerobj:DbHandler):
        self.empId = empId
        self.prId = prId
        response = self.getTicketDeatils(prId=prId, caller='edit', dbhandlerobj=dbhandlerobj)
        return response

    def viewTicket(self, prId, dbhandlerobj:DbHandler):
        response = self.getTicketDeatils(prId=prId, caller='view', dbhandlerobj=dbhandlerobj)
        return response

    def ticketDisplay(self, data):
        print('\n\n')
        mainMessage = ps.mainDisplay.format(data[2], data[0], data[1])
        Decorator().message(mainMessage)
        print("\n")

        if data[6] is not None:
            print(ps.desc.format(data[6].title()))
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

        print("\n\n")
        return 1

    def closeTicket(self, empId, prId, dbhandlerobj:DbHandler):
        self.empId = empId
        self.prId = prId
        response = self.getTicketDeatils(prId=prId, caller='close', dbhandlerobj=dbhandlerobj)
        return response

    def changeStatus(self, data, dbhandlerobj:DbHandler):

        self.ticketId = data[0]

        if data[5] == 'DONE':
            print(ps.ticketAlreadyClosed)
            return 1
        
        else:
            userInput = input(ps.closeConfirmation.format(data[1].capitalize(), data[0]))
            if userInput.lower() == 'y':
                respStatus = dbhandlerobj.editTicket(ticketId=self.ticketId, data=dbhandlerobj.getIndiviadualStatus('DONE'), what='status', why='close')
                if respStatus:
                    dbhandlerobj.changeDate(self.ticketId, which='r', what='add')
                    Decorator().message(ps.ticketCloseSuccess)
                    return 1
                else:
                    Decorator().message(ps.ticketCloseFail)
                    return 0
            else:
                print(ps.ticketNotClosed)
                return 0