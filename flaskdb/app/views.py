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

@app.route('/')
def index():
    connect = pymysql.connect(host='127.0.0.1', user=user, passwd=password, db=database)
    cursor = connect.cursor()
    sql_query = '''select *
                from User
                where is_active = 1
                order by Last_login_date
                limit 100'''
    print(sql_query)
    cursor.execute(sql_query)
    records = dictfetchall(cursor)
    return render_template('index.html', records = records, title = 'Home')