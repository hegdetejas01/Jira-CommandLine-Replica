from dbHandler import DbHandler

dbo = DbHandler()
orgId = 1
query = "SELECT COUNT(*) FROM employee WHERE org_id = %s"
dbo.cursor.execute(query, (orgId, ))
exists = dbo.cursor.fetchone()[0]
print(exists)