welcomeMessage = "Welcome To Jira"
clickExitMessage = "Click any charater to Exit"
getOrgName = "Enter the name of the organisation to register: "
adminSuccessAdd = "Employee with ID = {} Successfully added as Admin for Org Id = {}"
dbConnectionFailure = "Failed to Connect to DB. Restart the Program"
orgExists = "Organisation Already Registered. Try Logging In."
orgAddFailure = "Failed to Add to DB."
orgAddSuccess = "Organisation successfully added to DB"
insufficientEmpForAdm = "There are insufficent employees to be assigned as Admin... What would you like to do next??"
returnSuperAdmMainMenu = "Returning to main menu..."
maxAdmLimit = "Maximum Admin Limit for your Organisation Reached.! Click 1 to edit the admins (if needed)"
manMainMenu = """
1. Click 1 to add employees to project
2. Click 2 to remove employees from project
3. Click 3 to create ticket
4. Click 4 to edit ticket
5. Click 5 to view ticket
6. Click 6 to Logout
"""
superAdmMainMenu = """
1. Click 1 to assign admins
2. Click 2 to edit admins
3. Click 3 to create project
4. Click 4 to edit project information
5. Click 5 to Logout
"""
AdmMainMenu = """
1. Click 1 to create project
2. Click 2 to edit project information
3. Click 3 to Logout
"""
input1 = """
What do you want to do?
1. Click 1 to Login
2. Click 2 to Register
Click any character to Exit
"""
loginInput = """
1. Click 1 to Login
2. Click 2 to Go Back
Click any charater to Exit
"""
registerInput = """
1. Click 1 to Register as a Company
2. Click 2 to Register as an Employee
3. Click 3 to Go Back
Click any character to Exit
"""
empRegEmail = "Enter the email id of the employee to register: "
empPresent = "Employee Already Registered. Try Logging In"
printForAdmSelection = "Click {} to assign as admin {} ({})"
empAsAdmin = "Whom do you want to select as an admin? "
empRegName = "Enter the name of the employee: "
empPassword = "Enter the password: "
empRegFailed = "User Registration Failed"
empRegSuccess = "User Registered Successfully"
askOrg = "To Which Organisation You Belong To ?"
empDoesnotExist = "USER DOESNOT EXIST. TRY REGISTERING"
empCredMisMatch = "CREDENTIAL DOESNOT MATCH. TRY ONCE AGAIN"
superAdmRegisterSuccess = "SUCCESSFULLY ADDED YOU AS SUPER ADMIN"
superAdmLoginSuccess = "{} successfully logged in as Super Admin"
superAdminAssigned =  "You are the first employee from your ORGANISATION to get registered. Therefore, assigning you as the SUPER ADMIN"
adminLoginSuccess = "{} successfully logged in as General Admin"
empLoginSuccess = "{} successfully logged in"
manLoginSuccess = "{} successfully logged in as Manager"
logoutSuccess = "SUCCESSFULLY LOGGED-OUT FROM {} ACCOUNT"
printOrg = "Click {} for {}"
empLoginEmail = "Enter you email to Login: "
proName = "Enter the project name to create: "
manId = "Who is the manager for this project? "
noManForPro = "No Employees Present To Add them as managers"
manToPro = "Click {} to assign {} ({}) as manager to the project"
newManToPro = "Click {} to assign {} ({}) as the new manager to the project"
exitClick = "Click x or X to exit..."
proSuccessToDb = "Project Successfully Added to DB..."
proFailedToDb = "Failed to add project to DB... Try Again..."
invalidInput = "Invalid Input. Try Again... "
noAdmYet  = "No Admins in your organisation yet..."
admRemoveId = "Whom do you want to remove as Admin? "
editAdmOp = "Click {} to remove {} ({})"
admRemoveSuccess = "Successfully removed the adm with adm id = {}"
admRemoveFailure = "Failed to remove the admin... Try Again"
askEditProj = 'Which project you want to edit??'
projEditNum = "Click {} to edit the project with name '{}'"
askProjNameEdit = "Want to edit name of the project (current name = {}) (y/n): "
askProjNewName = "Enter the new name for the project: "
askManNameEdit = "Want to change the manager (current manager = {}) (y/n): "
manNotAvailable = "There are no employee available other than the current manager"
projEditSuccess = "Project edit successfull"
projEditFailed = "Failed to update the DB. Try again..."
empNotAvailableForAdmin = "No Free Empployees in your organisation to add them as admins. Try adding employees for your organisation first..."
projSelect = "Which project do you choose?"
projSelectDetail = "Click {} to select project with name {}"
noEmpForPr =  "There are no employees to add them to the project"
askEmpAdd = "\nSelect the employees you want to add. If you want to add multiple employee, enter the numbers space saperated..."
empForPr = "Click {} to select {} ({})"
invalidEmpInput = "Invalid Input ID -"
addEmpToWork = "\nAdding Employee {} to the selected project"
addEmpToWorkSuccess = "Employee with ID {} successfully added to the project"
addEmpToWorkFailure = "Employee with ID {} already present for the given project"
manOpsRedirect = "Redirecting to Main Menu due to one or more wrong input..."
removeEmpFromWork = "\nRemoving Employee {} to the selected project"
removeEmpFromWorkSuccess = "Employee with ID {} successfully removed to the project"
removeEmpFromWorkFailure = "Employee with ID {} not present in this project"
empInput = """
1. Click 1 to view ticket
2. Click 2 to create ticket
3. Click 3 to update ticket
4. Click 4 to close the ticket
5. Click 5 to logout
"""
empNotPresentInPr = "No Employees are yet present in the project... Try Adding the employees for the project first"
removeEmpFromPr = "\nWhom do you want to remove? If there are multiple employee keep it space saperated..."
removeEmpFromPrOptions = "Click {} to remove {} ({}) from this project (ID = {})"