import sqlite3

from models import db_path, Match

with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM Matches LIMIT 1')
    match = Match(cur.fetchone())
    match.save()
    test = 1
