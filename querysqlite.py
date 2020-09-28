from computervision.bossasql import SQLiteConn
SQLiteConn.connect()
#rows=SQLiteConn.get_last()
rows=SQLiteConn.get_all()
print(rows)
