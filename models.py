import os
import random
import sqlite3
from datetime import datetime

import pytz
from tzlocal import get_localzone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")


class Agent(object):

    def __init__(self, chromosome, learning=True) -> None:
        self.right = 0
        self.wrong = 0
        self.chromosome = chromosome
        self.learning = learning

    @property
    def accuracy(self):
        return float(self.right / (self.right + self.wrong))

    def guess(self, match):
        """

        :param match:
        :return:
        """
        red_score = 0
        blue_score = 0

        # if match.red_bet and match.blue_bet:
        #     red_score += match.red_bet * self.chromosome.bet
        #     blue_score += match.blue_bet * self.chromosome.bet
        #
        # if match.red_betters and match.blue_betters:
        #     red_score += match.red_betters * self.chromosome.betters
        #     blue_score += match.blue_betters * self.chromosome.betters
        #
        # red_score += match.red.avg_bet_ut(match.date) * self.chromosome.bet
        # blue_score += match.blue.avg_bet_ut(match.date) * self.chromosome.bet
        #
        # red_score += match.red.avg_betters_ut(match.date) * self.chromosome.betters
        # blue_score += match.blue.avg_betters_ut(match.date) * self.chromosome.betters
        #
        red_score += match.red.avg_odds_ut(match.date) * self.chromosome.odds
        blue_score += match.blue.avg_odds_ut(match.date) * self.chromosome.odds

        red_score += match.red.avg_time_win_ut(match.date) * self.chromosome.avg_win_time
        blue_score += match.blue.avg_time_win_ut(match.date) * self.chromosome.avg_win_time

        red_score += match.red.avg_time_loss_ut(match.date) * self.chromosome.avg_loss_time
        blue_score += match.blue.avg_time_loss_ut(match.date) * self.chromosome.avg_loss_time

        red_score += match.red.matches_ut(match.date) * self.chromosome.matches
        blue_score += match.blue.matches_ut(match.date) * self.chromosome.matches

        red_score += match.red.win_rate_tourn_ut(match.date) * self.chromosome.wins_t
        blue_score += match.blue.win_rate_tourn_ut(match.date) * self.chromosome.wins_t

        red_score += match.red.win_rate_exhib_ut(match.date) * self.chromosome.wins_e
        blue_score += match.blue.win_rate_exhib_ut(match.date) * self.chromosome.wins_e

        red_score += match.red.win_rate_match_ut(match.date) * self.chromosome.wins_m
        blue_score += match.blue.win_rate_match_ut(match.date) * self.chromosome.wins_m

        red_score += match.red.win_rate_tier_ut(match.date, match.tier) * self.chromosome.wins_tier
        blue_score += match.blue.win_rate_tier_ut(match.date, match.tier) * self.chromosome.wins_tier

        red_score += match.red.wins_against_ut(match.blue, match.date) * self.chromosome.wins_against
        blue_score += match.blue.wins_against_ut(match.red, match.date) * self.chromosome.wins_against

        try:
            if red_score > blue_score:
                guess = match.red
                confidence = red_score / (red_score + blue_score)
            else:
                guess = match.blue
                confidence = blue_score / (red_score + blue_score)
        except ZeroDivisionError:
            # May be their first match / not enough information
            if self.learning:
                return None  # for learning purposes - skip
            else:
                if random.randint(0, 1):
                    guess = match.red
                else:
                    guess = match.blue
                confidence = 0.5

        if self.learning:
            if guess == match.winner:
                return True
            else:
                return False
        else:
            return guess, confidence


class Fighter(object):

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id'] if kwargs.get('id') else None
        self.name = kwargs['name'] if kwargs.get('name') else ''
        super().__init__()

    def __str__(self):
        return self.name

    @property
    def tier(self):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT tier FROM Matches ORDER BY date DESC LIMIT 1')
            return cur.fetchone()[0]

    # @property
    # def avg_bet(self):
    #     rb = Match.objects.filter(red=self).aggregate(Avg('red_bet'))['red_bet__avg']
    #     bb = Match.objects.filter(blue=self).aggregate(Avg('blue_bet'))['blue_bet__avg']
    #     return (rb if rb else 0) + (bb if bb else 0)
    #
    # def avg_bet_ut(self, date):
    #     rb = Match.objects.filter(red=self, date__lt=date).aggregate(Avg('red_bet'))['red_bet__avg']
    #     bb = Match.objects.filter(blue=self, date__lt=date).aggregate(Avg('blue_bet'))['blue_bet__avg']
    #     return (rb if rb else 0) + (bb if bb else 0)
    #
    # @property
    # def avg_betters(self):
    #     rb = Match.objects.filter(red=self).aggregate(Avg('red_betters'))['red_betters__avg']
    #     bb = Match.objects.filter(blue=self).aggregate(Avg('blue_betters'))['blue_betters__avg']
    #     return (rb if rb else 0) + (bb if bb else 0)
    #
    # def avg_betters_ut(self, date):
    #     rb = Match.objects.filter(red=self, date__lt=date).aggregate(Avg('red_betters'))['red_betters__avg']
    #     bb = Match.objects.filter(blue=self, date__lt=date).aggregate(Avg('blue_betters'))['blue_betters__avg']
    #     return (rb if rb else 0) + (bb if bb else 0)
    #
    # @property
    # def avg_odds(self):
    #     rb = Match.objects.filter(red=self).aggregate(Avg('red_betters'))['red_betters__avg']
    #     bb = Match.objects.filter(blue=self).aggregate(Avg('blue_betters'))['blue_betters__avg']
    #     return (rb if rb else 0) + (bb if bb else 0)
    #
    # def avg_odds_ut(self, date):
    #     rb = Match.objects.filter(red=self, date__lt=date).aggregate(Avg('red_odds'))['red_odds__avg']
    #     bb = Match.objects.filter(blue=self, date__lt=date).aggregate(Avg('blue_odds'))['blue_odds__avg']
    #     return (rb if rb else 0) + (bb if bb else 0)
    #
    # @property
    # def avg_time_win(self):
    #     time = Match.objects.filter(winner=self).aggregate(Avg('time'))['time__avg']
    #     return time if time else 0
    #
    # def avg_time_win_ut(self, date):
    #     time = Match.objects.filter(winner=self, date__lt=date).aggregate(Avg('time'))['time__avg']
    #     return time if time else 0
    #
    # @property
    # def avg_time_loss(self):
    #     time = Match.objects.filter(~Q(winner=self), Q(red=self) | Q(blue=self)).aggregate(Avg('time'))['time__avg']
    #     return time if time else 0
    #
    # def avg_time_loss_ut(self, date):
    #     time = Match.objects.filter(Q(date__lte=date), ~Q(winner=self),
    #                                 Q(red=self) | Q(blue=self)).aggregate(Avg('time'))['time__avg']
    #     return time if time else 0
    #
    # @property
    # def matches(self):
    #     return Match.objects.filter(Q(red=self) | Q(blue=self)).count()
    #
    # def matches_ut(self, date):
    #     return Match.objects.filter(Q(date__lt=date), Q(red=self) | Q(blue=self)).count()
    #
    # @property
    # def wins(self):
    #     return self.win_fighter.count()
    #
    # def wins_ut(self, date):
    #     return Match.objects.filter(winner=self, date__lte=date).count()
    #
    # @property
    # def losses(self):
    #     return Match.objects.filter(~Q(winner=self), Q(red=self) | Q(blue=self)).count()
    #
    # def losses_ut(self, date):
    #     return Match.objects.filter(Q(date__lte=date), ~Q(winner=self), Q(red=self) | Q(blue=self)).count()
    #
    # @property
    # def win_rate(self):
    #     try:
    #         return round(self.wins / self.matches, 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # def win_rate_ut(self, date):
    #     try:
    #         return round(self.wins_ut(date) / self.matches_ut(date), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # @property
    # def win_rate_match(self):
    #     try:
    #         return round(Match.objects.filter(winner=self, mode=Match.MATCHMAKING).count() /
    #                      Match.objects.filter(Q(mode=Match.MATCHMAKING), Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # def win_rate_match_ut(self, date):
    #     try:
    #         return round(Match.objects.filter(date=date, winner=self, mode=Match.MATCHMAKING).count() /
    #                      Match.objects.filter(Q(date=date), Q(mode=Match.MATCHMAKING),
    #                                           Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # @property
    # def win_rate_exhib(self):
    #     try:
    #         return round(Match.objects.filter(winner=self, mode=Match.EXHIBITION).count() /
    #                      Match.objects.filter(Q(mode=Match.EXHIBITION), Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # def win_rate_exhib_ut(self, date):
    #     try:
    #         return round(Match.objects.filter(date=date, winner=self, mode=Match.EXHIBITION).count() /
    #                      Match.objects.filter(Q(date=date), Q(mode=Match.EXHIBITION),
    #                                           Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # @property
    # def win_rate_tourn(self):
    #     try:
    #         return round(Match.objects.filter(winner=self, mode=Match.TOURNAMENT).count() /
    #                      Match.objects.filter(Q(mode=Match.TOURNAMENT), Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # def win_rate_tourn_ut(self, date):
    #     try:
    #         return round(Match.objects.filter(date=date, winner=self, mode=Match.TOURNAMENT).count() /
    #                      Match.objects.filter(Q(date=date), Q(mode=Match.TOURNAMENT),
    #                                           Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # def win_rate_tier_ut(self, date, tier):
    #     try:
    #         return round(Match.objects.filter(winner=self, date__lt=date, tier=tier).count() /
    #                      Match.objects.filter(Q(date__lt=date), Q(tier=tier), Q(red=self) | Q(blue=self)).count(), 4)
    #     except ZeroDivisionError:
    #         return 0.5  # no matches
    #
    # def wins_against(self, fighter):
    #     return Match.objects.filter(Q(winner=self), Q(red=fighter) | Q(blue=fighter)).count()
    #
    # def wins_against_ut(self, fighter, date):
    #     return Match.objects.filter(Q(date__lt=date), Q(winner=self), Q(red=fighter) | Q(blue=fighter)).count()

    def create(self):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Fighters (name) VALUES ( ? )', self.name)

    def update(self):
        if not self.id:
            print('no ID')
            return
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Fighters (name) VALUES ( ? ) WHERE rowid = ?', (self.name, self.id))


class Match(object):
    MATCHMAKING = 'm'
    EXHIBITION = 'e'
    TOURNAMENT = 't'
    CURRENT_ID = 1

    def __init__(self, **kwargs):
        self.id = kwargs['id'] if kwargs.get('id') else None
        self.red = kwargs['red'] if kwargs.get('red') else ''
        self.blue = kwargs['blue'] if kwargs.get('blue') else ''
        self.winner = kwargs['winner'] if kwargs.get('winner') else ''
        self.tier = kwargs['tier'] if kwargs.get('tier') else ''
        self.time = kwargs['time'] if kwargs.get('time') else 0
        self.mode = kwargs['mode'] if kwargs.get('mode') else ''
        self.red_betters = kwargs['red_betters'] if kwargs.get('red_betters') else 0
        self.blue_betters = kwargs['blue_betters'] if kwargs.get('blue_betters') else 0
        self.red_bet = kwargs['red_bet'] if kwargs.get('red_bet') else 0
        self.blue_bet = kwargs['blue_bet'] if kwargs.get('blue_bet') else 0
        self.red_odds = kwargs['red_odds'] if kwargs.get('red_odds') else 0
        self.blue_odds = kwargs['blue_odds'] if kwargs.get('blue_odds') else 0
        self.date = kwargs['date'] if kwargs.get('date') else datetime.utcnow().replace(tzinfo=pytz.utc)\
            .astimezone(get_localzone())

    def __str__(self):
        return '{} v. {} ({})'.format(self.red, self.blue, 'Unkonwn' if not self.date else self.date.strftime('%m/%d/%Y %I:%M%p'))

    @classmethod
    def test_set_h(cls):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Matches ORDER BY random() LIMIT 100')
            for row in cur.fetchall():
                kwargs = {}
                for field, value in zip([description[0] for description in cur.description], row):
                    kwargs.update({field: value})
                yield cls(**kwargs)

    @classmethod
    def test_set(cls):
        return list(cls.test_set_h())

    def gen_odds(self):
        if self.red_bet > self.blue_bet:
            self.red_odds = round(float(self.red_bet) / float(self.blue_bet), 4)
            self.blue_odds = 1
        else:
            self.red_odds = 1
            self.blue_odds = round(float(self.blue_bet) / float(self.red_bet), 4)

    def get_odds(self):
        if not self.red_odds or not self.blue_odds:
            self.gen_odds()
        return '{} : {}'.format(self.red_odds, self.blue_odds)

    def create(self):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Matches (red, blue, winner, tier, mode, red_odds, blue_odds, '
                        'time, date) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )',
                        (self.red, self.blue, self.winner, self.tier, self.mode,
                         self.red_odds, self.blue_odds, self.time, self.date))

    def save(self):
        if not self.id:
            print('no ID')
            return
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Matches (red, blue, winner, tier, mode, red_odds, blue_odds, '
                        'time, date) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? ) WHERE rowid = ?',
                        (self.red, self.blue, self.winner, self.tier, self.mode,
                         self.red_odds, self.blue_odds, self.time, self.date, self.id))


class Chromosome(object):
    DEVIATION = 1

    def __init__(self, **kwargs):
        self.id = kwargs['id'] if kwargs.get('id') else None
        self.agent_score = kwargs['agent_score'] if kwargs.get('agent_score') else 0.5

        # weights
        self.bet = kwargs['bet'] if kwargs.get('bet') else self.__class__.initial_set()
        self.betters = kwargs['betters'] if kwargs.get('betters') else self.__class__.initial_set()
        self.odds = kwargs['odds'] if kwargs.get('odds') else self.__class__.initial_set()
        self.matches = kwargs['matches'] if kwargs.get('matches') else self.__class__.initial_set()
        self.wins_t = kwargs['wins_t'] if kwargs.get('wins_t') else self.__class__.initial_set()
        self.wins_e = kwargs['wins_e'] if kwargs.get('wins_e') else self.__class__.initial_set()
        self.wins_m = kwargs['wins_m'] if kwargs.get('wins_m') else self.__class__.initial_set()
        self.wins_tier = kwargs['wins_tier'] if kwargs.get('wins_tier') else self.__class__.initial_set()
        self.wins_against = kwargs['wins_against'] if kwargs.get('wins_against') else self.__class__.initial_set()
        self.avg_win_time = kwargs['avg_win_time'] if kwargs.get('avg_win_time') else self.__class__.initial_set()
        self.avg_loss_time = kwargs['avg_loss_time'] if kwargs.get('avg_loss_time') else self.__class__.initial_set()

    @classmethod
    def initial_set(cls):
        return random.uniform(-10, 10)

    def mutate(self):
        # mutation rate is 50%
        values = self.__dict__.copy()
        for field, value in values.items():
            if random.randint(0, 1):
                values.update({field: random.uniform(self.__getattribute__(field) - self.DEVIATION,
                                                     self.__getattribute__(field) + self.DEVIATION)})
        return Chromosome(**values).create()

    @classmethod
    def all_h(cls):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT rowid, * FROM Chromosomes')
            for row in cur.fetchall():
                kwargs = {}
                for field, value in zip([description[0] for description in cur.description], row):
                    kwargs.update({field: value})
                yield cls(**kwargs)

    @classmethod
    def all(cls):
        return list(cls.all_h())

    def create(self):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Chromosomes (agent_score, bet, betters, odds, matches, wins_t, wins_e, '
                        'wins_m, wins_tier, wins_against, avg_win_time, avg_loss_time) '
                        'VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )',
                        (self.agent_score, self.bet, self.betters, self.odds, self.matches,
                         self.wins_t, self.wins_e, self.wins_m, self.wins_tier, self.wins_against,
                         self.avg_win_time, self.avg_loss_time))

    def save(self):
        if not self.id:
            print('no ID')
            return
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Chromosomes (agent_score, bet, betters, odds, matches, wins_t, wins_e, '
                        'wins_m, wins_tier, wins_against, avg_win_time, avg_loss_time) '
                        'VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ) WHERE rowid = ?',
                        (self.agent_score, self.bet, self.betters, self.odds, self.matches,
                         self.wins_t, self.wins_e, self.wins_m, self.wins_tier, self.wins_against,
                         self.avg_win_time, self.avg_loss_time, self.id))

    def delete(self):
        if not self.id:
            print('no ID')
            return
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM Chromosomes WHERE rowid = {}'.format(self.id))

    @classmethod
    def delete_many(cls, ids=None):
        query = '(' + ', '.join([cid for cid in ids if cid is not None]) + ')'
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM Chromosomes WHERE rowid IN {}'.format(query))

    @classmethod
    def clean(cls):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM Chromosomes ORDER BY agent_score OFFSET 15')
