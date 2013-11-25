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
def index():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    sql_query = '''select *
                from User
                where is_active = 1
                order by Last_login_date DESC
                limit 100'''
    cursor.execute(sql_query)
    records = dictfetchall(cursor)
    return render_template('index.html', records=records)


@app.route('/user/<int:item_id>', methods=['GET'])
def detail_user(item_id=None):
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    sql_query = '''select *
                from GameCharacter
                where User_User_id=%(id)d''' % {'id': item_id}
    cursor.execute(sql_query)
    records = dictfetchall(cursor)
    return render_template('index.html', records = records)