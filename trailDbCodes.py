from dbHandler import DbHandler

dbo = DbHandler()

# orgId = "tejas@gmail.com"
# query = "SELECT COUNT(*) FROM employee WHERE org_id = (SELECT org_id FROM employee WHERE emp_email = %s)"
# dbo.cursor.execute(query, (orgId, ))
# exists = dbo.cursor.fetchone()[0]
# print(exists)

# email = 't'
# query = "SELECT emp_id FROM employee WHERE emp_email = %s"
# dbo.cursor.execute(query, (email, ))
# empId = dbo.cursor.fetchone()
# print(empId)

# empId = 13
# type='S'
# query = "INSERT INTO admin (adm_type, emp_id) VALUES (%s, %s)"
# insertTuple = (type, empId)
# dbo.cursor.execute(query, insertTuple)
# dbo.conn.commit() 
# print("INSERT SUCCESSFULL")

# email = 'a'
# query = "SELECT emp_id FROM employee WHERE emp_email = %s"
# dbo.cursor.execute(query, (email, ))
# empId = dbo.cursor.fetchone()[0]
# print("EMP ID = ", type(empId))

email = "tejas@gmail.com"
query = "SELECT emp_id, emp_password FROM employee WHERE emp_email = %s"
dbo.cursor.execute(query, (email, ))
empId = dbo.cursor.fetchone()
if empId:
    print("1", empId[0], empId[1])
else:
    print("0", empId[1])