#unicoding = utf-8

#from local.py
from local import user, password, database
import requests
import pymysql

USER_AMOUNT = 1000
CHARACTER_AMOUNT = 1000
MATCH_AMOUNT = 1000
SET_AMOUNT = 1000
ITEM_AMOUNT = 1000
CHARACTERISTICS_AMOUNT = 1000
ABILITY_AMOUNT = 1000
CLASS_AMOUNT = 1000

word_site = "http://www.freebsd.org/cgi/cvsweb.cgi/src/share/dict/web2?rev=1.12;content-type=text%2Fplain"

response = requests.get(word_site)
WORDS = response.content.splitlines()
print(WORDS)

connect = pymysql.connect(host='127.0.0.1', port=3306, user=user, passwd=password, db=database)
cursor = connect.cursor()
cursor.execute("SHOW TABLES")
print(cursor.description)
for row in cursor:
   print(row)
cursor.close()
connect.close()