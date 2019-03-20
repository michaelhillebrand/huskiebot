import sqlite3
import sys
from datetime import datetime

from models import db_path

"""
    THIS OVERWRITES DATABASE
"""

if __name__ == '__main__':
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        skip = 0
        with open(sys.argv[1], 'rb') as file:
            for row in file.readlines():
                try:
                    data = row.decode('ascii', errors='ignore').replace('\r\n', '').split(',')
                    odds = data[7].split(':')
                    cur.execute('INSERT INTO Matches (red, blue, winner, tier, mode, red_odds, blue_odds, time, date) '
                                'VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )',
                                (data[0], data[1], data[0] if data[2] == 0 else data[1], data[5], data[6],
                                 odds[0], odds[1], data[8], datetime.strptime(data[-1][:10], '%d-%m-%Y')))
                except IndexError:
                    skip += 1

        conn.commit()
        conn.close()
        print('Import Successful ({} skipped)'.format(skip))
    except IndexError:
        print('Import file not provided')
