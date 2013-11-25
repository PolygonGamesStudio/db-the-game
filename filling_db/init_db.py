import datetime
from random import choice, randint
import requests
import pymysql
#from local.py
from filling_db.local import user, password, database



USER_AMOUNT = 10000
GAME_CHARACTER_AMOUNT = 100000
GAME_MATCH_AMOUNT = 10000
GAMES_AMOUNT = 100000
SET_AMOUNT = 100000
ITEM_AMOUNT = 1000
CHARACTERISTICS_AMOUNT = 2000
ABILITY_AMOUNT = 100
CLASS_AMOUNT = 10
WORD_SITE = "http://www.freebsd.org/cgi/cvsweb.cgi/src/share/dict/web2?rev=1.12;content-type=text%2Fplain"
WORDS = []

User = ('User_id', 'Firstname', 'Lastname', 'Login', 'Password', 'Registration_date', 'Last_login_date', \
        'Birthday_date', 'Email', 'is_admin', 'is_active')
GameCharacter = ('Character_id', 'Name', 'Level', 'User_User_id', 'Characteristics_Characteristics_id', \
             'Class_Class_id')
Games = ('GameMatch_GameMatch_id', 'GameCharacter_GameCharacter_id')
GameMatch = ('GameMatch_id', 'Title', 'Date_begin', 'Date_end', 'Winner_id', 'Type')
Class = ('Class_id', 'Type')
Ability = ('Ability_id', 'Class_Class_id', 'Characteristics_Characteristics_id', 'Title', 'Description')
Characteristics = ('Characteristics_id', 'Health', 'Armor', 'Damage', 'Manna')
GameSet = ('GameSet_id', 'Head_Item_id', 'Body_Item_id', 'Special_Item_id', 'Weapon_Item_id', 'GameCharacter_GameCharacter_id')
Item = (
    'Item_id', 'Title', 'Description', 'GameCharacter_GameCharacter_id', 'Amount', 'Characteristics_Characteristics_id', 'Item_type')


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
        return choice(WORDS) + str(choice([x for x in range(100)])) + choice(WORDS) + choice(WORDS) + choice(WORDS) + str(choice([x for x in range(100)]))
    else:
        try:
            with open('filling_db/dictionary', encoding='utf-8') as dict_file:
                WORDS.extend(dict_file.read().splitlines())
        except IOError:
            response = requests.get(WORD_SITE)
            response.encoding = 'utf-8'
            with open('filling_db/dictionary', mode='w', encoding='utf-8') as dict_file:
                dict_file.write(response.text)
            WORDS.extend(response.text.splitlines())
        return choice(WORDS) + str(choice([x for x in range(10)])) + choice(WORDS) + choice(WORDS) + choice(WORDS) + str(choice([x for x in range(100)]))


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
        print(sql_query)
        cursor.execute(sql_query)
        return True
    except pymysql.DatabaseError as e:
        print(e)
        return False


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


def fill_class_table():
    for i in range(CLASS_AMOUNT):
        table_dict = {key: get_word_local() for key in Class}
        del table_dict['Class_id']
        fill_insert_sql(table_dict, 'Class')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


def fill_characteristics_table():
    for i in range(CHARACTERISTICS_AMOUNT):
        table_dict = {key: str(randint(0, 100)) for key in Characteristics}
        del table_dict['Characteristics_id']
        fill_insert_sql(table_dict, 'Characteristics')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


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


def fill_game_character_table():
    for i in range(GAME_CHARACTER_AMOUNT):
        table_dict = {key: get_word_local() for key in GameCharacter}
        del table_dict['Character_id']
        table_dict['Level'] = str(randint(1, 100))
        table_dict['User_User_id'] = str(randint(1, USER_AMOUNT))
        table_dict['Class_Class_id'] = str(randint(1, CLASS_AMOUNT))
        table_dict['Characteristics_Characteristics_id'] = str(randint(1, CHARACTERISTICS_AMOUNT))
        fill_insert_sql(table_dict, 'GameCharacter')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


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


def fill_game_set_table():
    for i in range(SET_AMOUNT):
        table_dict = {key: str(randint(1, ITEM_AMOUNT)) for key in GameSet}
        del table_dict['GameSet_id']
        table_dict['GameCharacter_GameCharacter_id'] = str(range(GAME_CHARACTER_AMOUNT))
        fill_insert_sql(table_dict, 'GameSet')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()


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



def fill_games_table():
    for i in range(GAMES_AMOUNT):
        #table_dict = {key: None for key in Games}
        table_dict = {}
        table_dict['GameMatch_GameMatch_id'] = str(randint(1, GAME_MATCH_AMOUNT))
        table_dict['GameCharacter_GameCharacter_id'] = str(randint(1, GAME_CHARACTER_AMOUNT))
        fill_insert_sql(table_dict, 'Games')
        #if i % COMMIT_AMOUNT == 0:
        #    connect.commit()
    connect.commit()

if __name__ == '__main__':
    #os.fork()
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()

    fill_user_table()
    fill_class_table()
    fill_characteristics_table()
    fill_ability_table()
    fill_game_character_table()
    fill_item_table()
    fill_game_set_table()
    fill_game_match_table()
    fill_games_table()

    connect.close()