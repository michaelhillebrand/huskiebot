import sqlite3


conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute('SELECT * FROM Matches WHERE red="!" OR blue="!"')
for row in cur:
    print(row)
conn.close()
