#unicoding = utf-8

#from local.py
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
        #return choice(WORDS).decode("utf-8") + choice(WORDS).decode("utf-8")  # FIXME: utf8 get
        return choice(WORDS) + choice(WORDS)
    else:
        response = requests.get(WORD_SITE)
        WORDS += response.content.splitlines().decode("utf-8")
        #return choice(WORDS).decode("utf-8") + choice(WORDS).decode("utf-8")
        return choice(WORDS) + choice(WORDS)


connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
cursor = connect.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.description)
for row in cursor:
    print(row)


def fill_user_table():
    for _ in itertools.repeat(None, USER_AMOUNT):
        first_name = get_word()
        last_name = get_word()
        login = get_word()
        passwd = get_word()
        now = datetime.datetime(2009, 5, 5)
        reg_date = now.date().isoformat()
        birth_date = now.date().isoformat()
        email = get_word() + '@' + get_word()
        is_admin = choice(['1', '2'])
        is_active = choice(['1', '2'])
        sql_query = """INSERT INTO User(Firstname,
                                        Lastname,
                                        Login,
                                        Password,
                                        Registration_date,
                                        Birthday_date,
                                        Email,
                                        is_admin,
                                        is_active)
                       VALUES ('{0}','{1}','{2}','{3}',{4},{5},'{6}','{7}','{8}')"""\
            .format(first_name, last_name, login, passwd, reg_date, birth_date, email, is_admin, is_active)
        print(sql_query)
        cursor.execute(sql_query)
    connect.commit()

if __name__ == '__main__':
    fill_user_table()
