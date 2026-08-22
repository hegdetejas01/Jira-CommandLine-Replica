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

# email = "tejas@gmail.com"
# query = "SELECT emp_id, emp_password FROM employee WHERE emp_email = %s"
# dbo.cursor.execute(query, (email, ))
# empId = dbo.cursor.fetchone()
# if empId:
#     print("1", empId[0], empId[1])
# else:
#     print("0", empId[1])

# emp_email = 'tejas@gmail.com'
# query = "select count(*) from admin as t1 inner join employee t2 on t1.emp_id = t2.emp_id WHERE t2.org_id = (SELECT org_id from employee WHERE emp_email = %s) AND t1.adm_type='A'"
# dbo.cursor.execute(query, (emp_email, ))
# exists = dbo.cursor.fetchone()[0]
# print(exists)

# emp_email = 'tejas@gmail.com'
# query = "select count(*) from employee where org_id = (select org_id from employee where emp_email = %s)"
# dbo.cursor.execute(query, (emp_email, ))
# exists = dbo.cursor.fetchone()[0]
# print(exists)

# org_id = 1
# query = "select t1.emp_id, t1.emp_email, t2.adm_type from employee t1 left join admin t2 on t1.emp_id = t2.emp_id where org_id = %s"
# dbo.cursor.execute(query, (org_id, ))
# for i in dbo.cursor:
#     if i[2] != 'S':
#         print(i[0],i[1], i[2])