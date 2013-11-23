#unicoding = utf-8
#!/usr/bin/env python

#from local.py
from local import user, password, database
import pymysql

connect = pymysql.connect(host='127.0.0.1', port=3306, user=user, passwd=password, db=database)
cursor = connect.cursor()
cursor.execute("SHOW TABLES")
print(cursor.description)
for row in cursor:
   print(row)
cursor.close()
connect.close()