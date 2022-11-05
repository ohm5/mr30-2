import json
from flask import Flask, request, send_from_directory
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
    cursor = query_db("SELECT * FROM courses WHERE course_num LIKE ? LIMIT 50", args=(f'%{course}%',))
    return list(map(dict, cursor))

course_suggestion("HIS")

@app.route('/')
def index():
    send_from_directory
    return send_from_directory('./fe/dist', 'index.html')

@app.route('/assets/<path:path>')
def assets(path):
    send_from_directory
    return send_from_directory('./fe/dist/assets', path)

@app.route('/sugg')
def sugg():
    q = request.args.get('q')

    if q is None:
        suggs = []
    else:
        suggs = course_suggestion(q)
        
        # FIXME do this in preprocess
        for sugg in suggs:
            sugg['course_t_start'] = f'{sugg["course_t_start"][:2]}:{sugg["course_t_start"][2:]}'
            sugg['course_t_end'] = f'{sugg["course_t_end"][:2]}:{sugg["course_t_end"][2:]}'

    return { 'results': suggs }, 200, {"Access-Control-Allow-Origin": "*"} # todo remove


if __name__ == "__main__":
    app.run()
