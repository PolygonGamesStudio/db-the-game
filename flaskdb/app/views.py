#coding: utf-8
from flask import render_template
import pymysql
from flaskdb.app import app
from filling_db.local import user, password, database


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


@app.route('/', methods=['GET'])
@app.route('/ratiolist', methods=['GET'])
def ratio_list():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    # самый крутых, больше побед
    sql_query = '''select GameCharacter_id,
            User_id,
            Login,
            Name,
            Level,
            Winner_id,
            Count_win
            from (
                select Winner_id,
                count(*) as Count_win
                from GameMatch
                group by Winner_id
                order by Count_win DESC
                limit 13
            ) as t
            join GameCharacter on t.winner_id = GameCharacter_id
            join User on User_User_id = User_id;
            '''
    cursor.execute(sql_query)
    records_count_win = dictfetchall(cursor)
    # количество игРАКОВ в классах
    sql_query = '''select Class_Class_id,
            Type,
            Count_class
            from (
                select Class_Class_id,
                count(*) as Count_class
                from GameCharacter
                group by Class_Class_id
                order by Count_class
                DESC limit 20
            ) as t
            join Class on Class_Class_id = Class_id;
                '''
    cursor.execute(sql_query)
    records_count_class = dictfetchall(cursor)
    # среднее кол-во жизни, брони, урона, манны для всех классов в игре
    sql_query = '''select Type,
                AVG(Health),
                AVG(Armor),
                AVG(Damage),
                AVG(Manna)
                from Ability
                join Class on Class_Class_id = Class_id
                join Characteristics on Characteristics_Characteristics_id = Characteristics_id
                group by Type;
                    '''
    cursor.execute(sql_query)
    records_avg_class = dictfetchall(cursor)
    return render_template('base_ratiolist.html', records_win=records_count_win, records_class=records_count_class, \
                           avg_class=records_avg_class)

@app.route('/userlist', methods=['GET'])
def user_list():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    # 100 последних активных пользователей
    sql_query = '''select
                    User_id,
                    Login,
                    Registration_date,
                    Last_login_date,
                    Email,
                    is_active
                    from User
                    where is_active = 1
                    order by Last_login_date DESC
                    limit 100;'''

    cursor.execute(sql_query)
    records = dictfetchall(cursor)
    return render_template('base_userlist.html', records=records)



@app.route('/user/<int:user_id>', methods=['GET'])
def user_detail(user_id=None):
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    # инфо о пользователе по id
    sql_query_to_get_user = '''
                                select User_id,
                                Firstname,
                                Lastname,
                                Login,
                                Password,
                                Registration_date,
                                Last_login_date,
                                Birthday_date,
                                Email,
                                is_admin,
                                is_active
                                from User
                                where User_id = %(id)d;
                            ''' % {'id': user_id}
    cursor.execute(sql_query_to_get_user)
    user_record = dict(zip([col[0] for col in cursor.description], cursor.fetchall()[0]))
    # все персонажи конкретного пользователя
    sql_query = '''
                    select GameCharacter_id,
                    Name,
                    Level,
                    User_User_id,
                    Characteristics_Characteristics_id,
                    Class_Class_id
                    from GameCharacter
                    where User_User_id=%(id)d
                    order by Level DESC;
                ''' % {'id': user_id}
    cursor.execute(sql_query)
    characters_record = dictfetchall(cursor)
    # последние матчи, в которых учавствовал user(т.е. все его персонажи)
    sql_query = '''
                select GameMatch_id,
                GameCharacter_id,
                Name,
                Title,
                Date_begin
                from Games join GameCharacter on GameCharacter_id = GameCharacter_GameCharacter_id
                join GameMatch on GameMatch_id = GameMatch_GameMatch_id
                where User_User_id = %(id)d
                order by Date_begin DESC
                limit 3;
                    ''' % {'id': user_id}
    cursor.execute(sql_query)
    matchs_record = dictfetchall(cursor)
    return render_template('base_user_by_id.html', user=user_record, characters=characters_record, matchs=matchs_record)


@app.route('/character/<int:character_id>', methods=['GET'])
def character_detail(character_id=None):
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    # статы персонажа
    sql_query = '''
    select User_id,
                Login,
                GameCharacter_id,
                Name,
                Level,
                Type
                from GameCharacter
                join Class on Class_Class_id = Class_id
                join User on User_id = User_User_id
                where GameCharacter_id = %(id)d;
                        ''' % {'id': character_id}
    cursor.execute(sql_query)
    character_record = dict(zip([col[0] for col in cursor.description], cursor.fetchall()[0]))
    # самый сильный предмет у персонажа
    sql_query = '''
                        select Item_id,
                        Title,
                        max(Health + Armor + Damage + Manna)
                        from Characteristics
                        join Item on Characteristics_Characteristics_id = Characteristics_id
                        where GameCharacter_GameCharacter_id = %(id)d;
                            ''' % {'id': character_id}
    cursor.execute(sql_query)
    super_item_record = dict(zip([col[0] for col in cursor.description], cursor.fetchall()[0]))
    # последние три боя, в которых он учавствовал
    sql_query = '''
                select GameMatch_id,
                GameCharacter_id,
                Name,
                Title,
                Date_begin
                from Games join GameCharacter on GameCharacter_id = GameCharacter_GameCharacter_id
                join GameMatch on GameMatch_id = GameMatch_GameMatch_id
                where GameCharacter_id = %(id)d
                order by Date_begin DESC
                limit 3;
                    ''' % {'id': character_id}
    cursor.execute(sql_query)
    matchs_record = dictfetchall(cursor)
    # шесть предметов конкретного персонажа
    sql_query = '''
                    select
                    Title,
                    Description,
                    Health,
                    Armor,
                    Damage,
                    Manna
                    from Item
                    join Characteristics on Characteristics_Characteristics_id = Characteristics_id
                    where GameCharacter_GameCharacter_id = %(id)d
                    limit 6;
                ''' % {'id': character_id}
    cursor.execute(sql_query)
    items_record = dictfetchall(cursor)
    # матчи, в которых персонаж выиграл (через таблицу для многие-ко-многим)
    sql_query = '''
                    select GameMatch_id,
                    GameCharacter_id,
                    Name,
                    Title,
                    Date_begin
                    from Games join GameCharacter on GameCharacter_id = GameCharacter_GameCharacter_id
                    join GameMatch on GameMatch_id = GameMatch_GameMatch_id
                    where Winner_id = %(id)d
                    group by Title
                    order by Date_begin DESC
                    limit 3;
                        ''' % {'id': character_id}
    cursor.execute(sql_query)
    win_matchs_record = dictfetchall(cursor)
    return render_template('base_character_by_id.html', matchs=matchs_record, win_matchs=win_matchs_record,\
                           items=items_record, character=character_record, super_item=super_item_record)


@app.route('/match/<int:match_id>', methods=['GET'])
def match_detail(match_id=None):
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    # инфа о матче по id, кто в нём учавствует и каких классов
    sql_query = '''
            select GameMatch_id,
            Title,
            Date_begin,
            Date_end,
            GameCharacter_id,
            Type,
            Name,
            Level
            from (
                select GameMatch_id,
                Title,
                Date_begin,
                Date_end
                from GameMatch where GameMatch_id = %(id)d
            ) as t
            join Games on  GameMatch_GameMatch_id = GameMatch_id
            join GameCharacter on GameCharacter_GameCharacter_id = GameCharacter_id
            join Class on Class_Class_id = Class_id;
                        ''' % {'id': match_id}
    cursor.execute(sql_query)
    match_record = dictfetchall(cursor)
    return render_template('base_match_by_id.html', match=match_record[0], match_users=match_record)

@app.route('/matchlist', methods=['GET'])
def match_list():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    # последние 100 матчей по времени окончания матча
    sql_query = '''select GameMatch_id,
                    Title,
                    Type,
                    Name,
                    Level,
                    Winner_id,
                    Date_end
                    from (
                        select GameMatch_id,
                        Title,
                        Type,
                        Winner_id,
                        Date_end
                        from GameMatch
                        order by Date_end DESC
                        limit 100
                    ) as t
                    join GameCharacter on GameCharacter_id = Winner_id
                    order by Date_end DESC;
            '''
    cursor.execute(sql_query)
    match_records = dictfetchall(cursor)
    return render_template('base_matchlist.html', matchs=match_records)
