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

# orgId= 0
# query = "select t1.adm_id, t2.emp_email, t2.emp_name from admin t1 inner join employee t2 on t1.emp_id = t2.emp_id WHERE t2.org_id = %s AND t1.adm_type='A'"
# dbo.cursor.execute(query, (orgId, ))
# data = dbo.cursor.fetchall()
# print(len(data))
# print(data)

# prName = 'Working'
# manId = 18
# query =  "INSERT INTO project (pr_name, emp_id) VALUES (%s, %s)"
# dbo.cursor.execute(query, (prName, manId))
# dbo.conn.commit()

# org_id = 1
# empIds = []
# query = "select t1.emp_id, t1.emp_email, t2.adm_type, t1.emp_name from employee t1 left join admin t2 on t1.emp_id = t2.emp_id where org_id = %s"
# dbo.cursor.execute(query, (org_id, ))
# datas = dbo.cursor.fetchall()
# for data in datas:
#     if data[2] != 'S' and data[2] != 'A':
#         empIds.append(data[0])
# print(empIds)

# manId = set()
# query = "select emp_id from project"
# dbo.cursor.execute(query)
# ids = dbo.cursor.fetchall()
# for id in ids:
#     manId.add(id[0])
# print(17 in manId)

# orgId = 1
# query = "select t1.pr_id, t1.pr_name, t2.emp_name, t2.emp_id from project t1 left join employee t2 on t1.emp_id = t2.emp_id where t2.org_id=%s"
# dbo.cursor.execute(query,(orgId, ))
# print(dbo.cursor.fetchall())

# email = "gansh@gmail.com"
# query = "select 1 from employee t1 left join project t2 on t1.emp_id = t2.emp_id where t1.emp_email=%s"
# dbo.cursor.execute(query, (email,))
# if dbo.cursor.fetchone():  print("Present")
# else: print("Not Present")

# email = 'tejs@gmail.com'
# query = "select emp_id from employee where emp_email=%s"
# dbo.cursor.execute(query, (email,  ))
# print(dbo.cursor.fetchone()[0])\

# prName = 'mangalyaan'
# query = "Select pr_id from project where pr_name = %s"
# dbo.cursor.execute(query, (prName,))
# print(dbo.cursor.fetchone()[0])

# prName = "gaganyaan"
# empId = 35
# dbo.cursor.execute("select pr_id from project where pr_name = %s", (prName, ))
# prId = dbo.cursor.fetchone()[0]
# query = "INSERT INTO work (emp_id, pr_id) VALUES (%s, %s)"
# dbo.cursor.execute(query, (empId, prId))
# dbo.conn.commit()

# prId = 105
# query = "select t1.emp_id, t1.emp_name, t1.emp_email from employee t1 right join work t2 on t1.emp_id = t2.emp_id where t2.pr_id = %s"
# dbo.cursor.execute(query, (prId, ))
# print(len(dbo.cursor.fetchall()))

# emp_id = 34
# query = "select pr_id, pr_name from project where emp_id=%s"
# dbo.cursor.execute(query, (emp_id, ))
# print(dbo.cursor.fetchall())

# query = "select id from tickets_status where status='TO DO'"
# dbo.cursor.execute(query)
# print(dbo.cursor.fetchone()[0])

# prId = 22
# query = "select pr_name from project where pr_id=%s"
# dbo.cursor.execute(query, (prId, ))
# print(dbo.cursor.fetchone()[0])

# prId = 22
# query = "select id from ticket where pr_id = %s ORDER BY id DESC LIMIT 1"
# try:
#     dbo.cursor.execute(query, (prId, ))
#     print(dbo.cursor.fetchone()[0])
# except Exception as e:
#     print(e)

# num = 149
# padded = f"{num:04d}"
# print(type(padded))
# print(padded)

id = 2
query = "select t1.ticket_id, t1.title, t2.pr_name, t7.type, t5.priority, t6.status, t1.description, t3.emp_name as assignee, t4.emp_name as created_by, t1.created_date, t1.modified_date, t1.resolved_date from ticket t1 left join project t2 on t1.pr_id = t2.pr_id left join employee t3 on t1.assignee = t3.emp_id left join employee t4 on t1.created_by = t4.emp_id left join tickets_priority t5 on t1.priority=t5.id left join tickets_status t6 on t1.ticket_status=t6.id left join tickets_type t7 on t1.ticket_type=t7.id where t1.id=%s"
dbo.cursor.execute(query, (id, ))
print(dbo.cursor.fetchall())