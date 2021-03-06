#coding: utf-8
import os, hashlib
import time
from random import choice, randint
import datetime

import pymysql
import requests
from filling_db.local import user, password, database

MIN = 1000
FORK_AMOUNT = 1

USER_AMOUNT = 1 * MIN
GAME_CHARACTER_AMOUNT = 3 * MIN
GAME_MATCH_AMOUNT = 1 * MIN
GAMES_AMOUNT = 3 * MIN
SET_AMOUNT = 4 * MIN
ITEM_AMOUNT = 5 * MIN
CHARACTERISTICS_AMOUNT = 5 * MIN * FORK_AMOUNT  # необходимо предварительное выполнение
ABILITIES = (
    'Fireball', 'Blessing', 'Bash', 'Wraith', 'Snowfall', 'Frostbite Bolt', 'Fire Blast', 'Resurrection', 'Curse',
    'Invisibility', 'Blizzard')
ABILITY_AMOUNT = len(ABILITIES)
CLASSES = (
    'Fighter', 'Thief', 'Scout', 'Engineer', 'Sniper', 'Medic', 'Spy', 'Captain', 'Demolition', 'Miner', 'Paladin',
    'Necromancer', 'Warlock')
CLASS_AMOUNT = len(CLASSES)
WORD_SITE = "http://www.freebsd.org/cgi/cvswe" \
            "b.cgi/src/share/dict/web2?rev=1.12;content-type=text%2Fplain"
WORDS = []

User = ('User_id', 'Firstname', 'Lastname', 'Login', 'Password', 'Registration_date', 'Last_login_date', \
        'Birthday_date', 'Email', 'is_admin', 'is_active')
GameCharacter = ('GameCharacter_id', 'Name', 'Level', 'User_User_id', 'Characteristics_Characteristics_id', \
                 'Class_Class_id')
Games = ('GameMatch_GameMatch_id', 'GameCharacter_GameCharacter_id')
GameMatch = ('GameMatch_id', 'Title', 'Date_begin', 'Date_end', 'Winner_id', 'Type')
Class = ('Class_id', 'Type')
Ability = ('Ability_id', 'Class_Class_id', 'Characteristics_Characteristics_id', 'Title', 'Description')
Characteristics = ('Characteristics_id', 'Health', 'Armor', 'Damage', 'Manna')
GameSet = (
    'GameSet_id', 'Head_Item_id', 'Body_Item_id', 'Special_Item_id', 'Weapon_Item_id', 'GameCharacter_GameCharacter_id')
Item = (
    'Item_id', 'Title', 'Description', 'GameCharacter_GameCharacter_id', 'Amount', 'Characteristics_Characteristics_id',
    'Item_type')


def how_long(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print("time: {0}".format(time.time() - t))
        return res

    return tmp


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
        return choice(WORDS) + hashlib.sha1(os.urandom(512)).hexdigest()[7:15]
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
        return choice(WORDS) + hashlib.sha1(os.urandom(512)).hexdigest()[7:15]


def get_date():
    year = choice(range(1950, 2013))
    month = choice(range(1, 12))
    day = choice(range(1, 28))
    date = datetime.datetime(year, month, day)
    return str(date)  # transfer datetime value to a str value


def get_one_or_zero():
    return choice(['0', '1'])


def fill_insert_sql(column_dict, table):
    try:
        sql_query = 'INSERT INTO ' + str(table) + "(" + ", ".join(column_dict.keys()) + ")" + ' VALUES ("' + \
                    '" , "'.join(column_dict.values()) + '")'
        # print(sql_query)
        cursor.execute(sql_query)
        return True
    except pymysql.DatabaseError as e:
        print(e)
        return False

@how_long
def fill_user_table():
    for i in range(USER_AMOUNT):
        table_dict = {key: get_word_local() for key in User}
        del table_dict['User_id'], table_dict['is_admin'], table_dict['is_active'], table_dict['Last_login_date']
        table_dict['Registration_date'] = get_date()
        table_dict['Birthday_date'] = get_date()
        table_dict['Email'] = get_word_local() + '@' + get_word_local()
        fill_insert_sql(table_dict, 'User')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_class_table():
    for game_class in CLASSES:
        table_dict = {key: game_class for key in Class}
        del table_dict['Class_id']
        fill_insert_sql(table_dict, 'Class')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_characteristics_table():
    for i in range(CHARACTERISTICS_AMOUNT):
        table_dict = {key: str(randint(0, 100)) for key in Characteristics}
        del table_dict['Characteristics_id']
        fill_insert_sql(table_dict, 'Characteristics')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_ability_table():
    for i in range(ABILITY_AMOUNT):
        table_dict = {key: get_word_local() for key in Ability}
        del table_dict['Ability_id']
        table_dict['Class_Class_id'] = str(randint(1, CLASS_AMOUNT))
        table_dict['Characteristics_Characteristics_id'] = str(randint(1, CHARACTERISTICS_AMOUNT))
        fill_insert_sql(table_dict, 'Ability')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_game_character_table():
    for i in range(GAME_CHARACTER_AMOUNT):
        table_dict = {key: get_word_local() for key in GameCharacter}
        del table_dict['GameCharacter_id']
        table_dict['Level'] = str(randint(1, 100))
        table_dict['User_User_id'] = str(randint(1, USER_AMOUNT))
        table_dict['Class_Class_id'] = str(randint(1, CLASS_AMOUNT))
        table_dict['Characteristics_Characteristics_id'] = str(randint(1, CHARACTERISTICS_AMOUNT))
        fill_insert_sql(table_dict, 'GameCharacter')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_item_table():
    for i in range(ITEM_AMOUNT):
        table_dict = {key: get_word_local() for key in Item}
        del table_dict['Item_id']
        table_dict['GameCharacter_GameCharacter_id'] = str(randint(1, GAME_CHARACTER_AMOUNT))
        table_dict['Amount'] = str(randint(1, 1000))
        table_dict['Characteristics_Characteristics_id'] = str(randint(1, CHARACTERISTICS_AMOUNT))
        table_dict['Item_type'] = str(randint(1, 1000))
        fill_insert_sql(table_dict, 'Item')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_game_set_table():
    for i in range(SET_AMOUNT):
        table_dict = {key: str(randint(1, ITEM_AMOUNT)) for key in GameSet}
        del table_dict['GameSet_id']
        table_dict['GameCharacter_GameCharacter_id'] = str(randint(1, GAME_CHARACTER_AMOUNT))
        fill_insert_sql(table_dict, 'GameSet')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_game_match_table():
    for i in range(GAME_MATCH_AMOUNT):
        table_dict = {key: get_word_local() for key in GameMatch}
        del table_dict['GameMatch_id']
        table_dict['Winner_id'] = str(randint(1, GAME_CHARACTER_AMOUNT))
        table_dict['Date_begin'] = get_date()
        table_dict['Date_end'] = get_date()
        fill_insert_sql(table_dict, 'GameMatch')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


@how_long
def fill_games_table():
    for i in range(GAMES_AMOUNT):
        #table_dict = {key: None for key in Games}
        table_dict = {'GameMatch_GameMatch_id': str(randint(1, GAME_MATCH_AMOUNT)),
                      'GameCharacter_GameCharacter_id': str(randint(1, GAME_CHARACTER_AMOUNT))}
        fill_insert_sql(table_dict, 'Games')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


if __name__ == '__main__':
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()

    fill_class_table()
    print("classes were added")
    fill_characteristics_table()
    print("characteristics were added")
    fill_ability_table()
    print("abilities were added")
    connect.close()

    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    fill_user_table()
    print("users were added")

    fill_game_character_table()
    print("characters were added")
    fill_item_table()
    print("items were added")
    fill_game_set_table()
    print("sets were added")
    fill_game_match_table()
    print("matches were added")
    fill_games_table()
    print("games were added with players")
    connect.close()
