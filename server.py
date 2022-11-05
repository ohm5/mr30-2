import json
from flask import Flask, request
import sqlite3

app = Flask(__name__)

DATABASE = './mr30.sqlite3'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    return db


def query_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.close()
    return rv


def course_suggestion(course):
    cursor = query_db("SELECT * FROM courses WHERE course_num LIKE ?", args=(f'%{course}%',))
    return list(map(dict, cursor))

course_suggestion("HIS")

@app.route('/')
def index():
    return {'index': 'page'}

@app.route('/sugg')
def sugg():
    q = request.args.get('q')

    if q is None:
        suggs = []
    else:
        suggs = course_suggestion(q)

    return { 'result': suggs }

app.run()
