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

User = ('User_id', 'Firstname', 'Lastname', 'Login', 'Password', 'Registration_date', 'Last_login_date', \
        'Birthday_date', 'Email', 'is_admin', 'is_active')
Character = ('Character_id', 'Name', 'Level', 'User_User_id', 'Characteristics_Characteristics_id', \
             'Class_Class_id')
Games = ('Match_Match_id', 'Character_Character_id')
Match = ('Match_id', 'Title', 'Date_begin', 'Date_end', 'Winner_id', 'Type')
Class = ('Class_id', 'Type')
Ability = ('Ability_id', 'Class_Class_id', 'Characteristics_Characteristics_id', 'Title', 'Description')
Characteristics = ('Characteristics_id', 'Heath', 'Armor', 'Damage', 'Manna')
Set = ('Set_id', 'Head_Item_id', 'Body_Item_id1', 'Special_Item_id2', 'Weapon_Item_id3', 'Character_Character_id')
Item = (
    'Item_id', 'Title', 'Title', 'Character_Character_id', 'Amount', 'Characteristics_Characteristics_id', 'Item_type')


def get_word():
    global WORDS
    if WORDS:
        return choice(WORDS) + choice(WORDS)
    else:
        response = requests.get(WORD_SITE)
        response.encoding = 'utf-8'
        #WORDS += response.text.splitlines()
        WORDS.extends(response.text.splitlines())
        return choice(WORDS) + choice(WORDS)


def get_word_local():
    global WORDS
    if WORDS:
        return choice(WORDS) + choice(WORDS)
    else:
        try:
            with open('dictionary', encoding='utf-8') as dict_file:
                WORDS.extend(dict_file.read().splitlines())
        except IOError:
            response = requests.get(WORD_SITE)
            response.encoding = 'utf-8'
            with open('dictionary', mode='w', encoding='utf-8') as dict_file:
                dict_file.write(response.text)
            WORDS.extend(response.text.splitlines())
        return choice(WORDS) + choice(WORDS)


connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
cursor = connect.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.description)
for row in cursor:
    print(row)


def fill_insert_sql(column_dict, table):
    try:
        sql_query = 'INSERT INTO ' + str(table) + "(" + ", ".join(column_dict.keys()) + ")" + ' VALUES "' + \
                    '" , "'.join(column_dict.values()) + '")'
        print(sql_query)
        cursor.execute(sql_query)
        connect.commit()
        return True
    except ProgrammingError:
        return False

if __name__ == '__main__':
    fill_insert_sql({"first_name": "alexei", "last_name": 'maratlanov', 'is_active': '1'}, 'User')