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


@app.route('/userlist', methods=['GET'])
def user_list():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
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
                limit 100'''

    cursor.execute(sql_query)
    # print cursor.description
    # print cursor.fetchall()
    # for desc in cursor.description:
    #     print(desc[0])
    records = dictfetchall(cursor)
    return render_template('base_userlist.html', records=records)


@app.route('/user/<int:user_id>', methods=['GET'])
def user_detail(user_id=None):
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    sql_query_to_get_user = '''
                                select
                                    User_id,
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
                                where User_id = %(id)d
                            ''' % {'id': user_id}
    cursor.execute(sql_query_to_get_user)
    user_record = dict(zip([col[0] for col in cursor.description], cursor.fetchall()[0]))
    sql_query = '''
                    select
                        GameCharacter_id,
                        Name,
                        Level,
                        User_User_id,
                        Characteristics_Characteristics_id,
                        Class_Class_id
                    from GameCharacter
                    where User_User_id=%(id)d
                ''' % {'id': user_id}
    cursor.execute(sql_query)
    # for desc in cursor.description:
    #     print(desc[0])
    characters_record = dictfetchall(cursor)

    return render_template('base_user_by_id.html', user=user_record, characters=characters_record)


@app.route('/games', methods=['GET'])
def war_list():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    sql_query = '''select *
                    from GameMatch
                    order by Date_begin DESC
                    limit 100'''
    cursor.execute(sql_query)
    records = dictfetchall(cursor)
    return render_template('index.html', records=records)
