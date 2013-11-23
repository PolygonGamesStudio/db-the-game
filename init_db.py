#unicoding = utf-8

#from local.py
from _sqlite3 import ProgrammingError
import datetime
import itertools
from random import choice
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
WORD_SITE = "http://www.freebsd.org/cgi/cvsweb.cgi/src/share/dict/web2?rev=1.12;content-type=text%2Fplain"
WORDS = []


def get_word():
    global WORDS
    if WORDS:
        return str(choice(WORDS)) + str(choice(WORDS))
    else:
        response = requests.get(WORD_SITE)
        WORDS += response.content.splitlines()
        return str(choice(WORDS)) + str(choice(WORDS))


connect = pymysql.connect(host='127.0.0.1', port=3306, user=user, passwd=password, db=database)
cursor = connect.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.description)
for row in cursor:
    print(row)


def fill_insert_sql(column_dict, table ):
    try:
        sql_query = 'INSERT INTO '+str(table)+"(" + ", ".join(column_dict.keys()) + ")" + ' VALUES "' +\
            '" , "'.join(column_dict.values()) + '")'
        print(sql_query)
        cursor.execute(sql_query)
        connect.commit()
        return True
    except ProgrammingError:
        return False

if __name__ == '__main__':
    fill_insert_sql({"first_name": "alexei", "last_name": 'maratlanov', 'is_active': '1'}, 'User')
