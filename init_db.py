#from local.py
from _sqlite3 import ProgrammingError
import datetime
import itertools
from random import choice, randint
from local import user, password, database
import requests
import pymysql


USER_AMOUNT = 1000
CHARACTER_AMOUNT = 1000
MATCH_AMOUNT = 1000
SET_AMOUNT = 1000
ITEM_AMOUNT = 1000
CHARACTERISTICS_AMOUNT = 100
ABILITY_AMOUNT = 1000
CLASS_AMOUNT = 10
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
Characteristics = ('Characteristics_id', 'Health', 'Armor', 'Damage', 'Manna')
Set = ('Set_id', 'Head_Item_id', 'Body_Item_id1', 'Special_Item_id2', 'Weapon_Item_id3', 'Character_Character_id')
Item = (
    'Item_id', 'Title', 'Title', 'Character_Character_id', 'Amount', 'Characteristics_Characteristics_id', 'Item_type')


def get_word_local():
    """
    функция возвращает слово, состоящее из двух слов, выбранных случайно
    слова выбираются из List-а
    List формируется из файла, если он существует
    если нет - из интернета, создавая при этом файл,
    чтобы в следующий раз не обращаться в инет
    """
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


def get_date():
    year = choice(range(1950, 2013))
    month = choice(range(1, 12))
    day = choice(range(1, 28))
    date = datetime.datetime(year, month, day)
    return str(date)  # transfer datetime value to a str value


def get_one_or_zero():
    return choice(['0', '1'])


connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
cursor = connect.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.description)
for row in cursor:
    print(row)


def fill_insert_sql(column_dict, table):
    try:
        sql_query = 'INSERT INTO ' + str(table) + "(" + ", ".join(column_dict.keys()) + ")" + ' VALUES ("' + \
                    '" , "'.join(column_dict.values()) + '")'
        print(sql_query)
        cursor.execute(sql_query)
        return True
    except ProgrammingError:
        return False


def fill_user_table():
    for _ in itertools.repeat(None, USER_AMOUNT):
        table_dict = {key: get_word_local() for key in User}
        del table_dict['User_id'], table_dict['is_admin'], table_dict['is_active'], table_dict['Last_login_date']
        table_dict['Registration_date'] = get_date()
        table_dict['Birthday_date'] = get_date()
        table_dict['Email'] = get_word_local() + '@' + get_word_local()
        fill_insert_sql(table_dict, 'User')
    connect.commit()


def fill_class_table():
    for _ in itertools.repeat(None, CLASS_AMOUNT):
        table_dict = {key: get_word_local() for key in Class}
        del table_dict['Class_id']
        fill_insert_sql(table_dict, 'Class')
    connect.commit()


def fill_characteristics_table():
    for _ in itertools.repeat(None, CHARACTERISTICS_AMOUNT):
        table_dict = {key: str(randint(0, 100)) for key in Characteristics}
        del table_dict['Characteristics_id']
        fill_insert_sql(table_dict, 'Characteristics')
    connect.commit()

def fill_ability_table():
    for _ in itertools.repeat(None, CHARACTERISTICS_AMOUNT):
        table_dict = {key: get_word_local() for key in Ability}
        del table_dict['Ability_id']
        table_dict['Class_Class_id'] = str(randint(1, CLASS_AMOUNT))
        table_dict['Characteristics_Characteristics_id'] = str(randint(1, CHARACTERISTICS_AMOUNT))
        fill_insert_sql(table_dict, 'Ability')


if __name__ == '__main__':
    fill_user_table()
    fill_class_table()
    fill_characteristics_table()
    fill_ability_table()
