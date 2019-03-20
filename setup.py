import sqlite3

from models import Chromosome

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Matches')
cur.execute('CREATE TABLE Matches (red TEXT, blue TEXT, '
            'winner TEXT, tier TEXT, time INTEGER, mode TEXT, red_betters INTEGER, blue_betters INTEGER, '
            'red_bet INTEGER, blue_bet INTEGER, red_odds REAL, blue_odds REAL, date DATE)')
cur.execute('DROP TABLE IF EXISTS Chromosomes')
cur.execute('CREATE TABLE Chromosomes (agent_score REAL, bet REAL, betters REAL, odds REAL, matches REAL, '
            'wins_t REAL, wins_e REAL, wins_m REAL, wins_tier REAL, wins_against REAL, '
            'avg_win_time REAL, avg_loss_time REAL)')
for n in range(30):
    Chromosome().create()
conn.commit()
conn.close()
