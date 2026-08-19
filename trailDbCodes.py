from dbHandler import DbHandler

dbo = DbHandler()

query = "SELECT emp_password FROM employee WHERE emp_email = %s"
email = "tejas@gmail.com"
dbo.cursor.execute(query, (email, ))
print(dbo.cursor.fetchone()[0])