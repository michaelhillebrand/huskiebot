import os
import random
import sqlite3
from datetime import datetime

import pytz
from tzlocal import get_localzone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")


def initial_set():
    return random.uniform(-10, 10)


# class Fighter(object):
#
#     def __init__(self) -> None:
#         self.name = 1
#         super().__init__()
#
#     def __str__(self):
#         return self.name
#
    # @property
    # def tier(self):
    #     rm = Match.objects.all().order_by('-date').first()
    #     if rm:
    #         return rm.tier
    #     else:
    #         return None
    #
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


class Match(object):
    MATCHMAKING = 'm'
    EXHIBITION = 'e'
    TOURNAMENT = 't'
    CURRENT_ID = 1

    def __init__(self, **kwargs):
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
    def test_set(cls):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Matches ORDER BY random() LIMIT 100')
            return [row for row in cur]

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

    def save(self):
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO Matches (red, blue, winner, tier, mode, red_odds, blue_odds, '
                        'time, date) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )',
                        (self.red, self.blue, self.winner, self.tier, self.mode,
                         self.red_odds, self.blue_odds, self.time, self.date))


# class Chromosome(object):
#     DEVIATION = 1
#
#     def __init__(self, **kwargs):
#         self.agent_score = kwargs['agent_score'] if kwargs.get('agent_score') else 0.5
#
#         # weights
#         self.bet = kwargs['bet'] if kwargs.get('bet') else initial_set()
#         self.betters = kwargs['betters'] if kwargs.get('betters') else initial_set()
#         self.odds = kwargs['odds'] if kwargs.get('odds') else initial_set()
#         self.matches = kwargs['matches'] if kwargs.get('matches') else initial_set()
#         self.wins_t = kwargs['wins_t'] if kwargs.get('wins_t') else initial_set()
#         self.wins_e = kwargs['wins_e'] if kwargs.get('wins_e') else initial_set()
#         self.wins_m = kwargs['wins_m'] if kwargs.get('wins_m') else initial_set()
#         self.wins_tier = kwargs['wins_tier'] if kwargs.get('wins_tier') else initial_set()
#         self.wins_against = kwargs['wins_against'] if kwargs.get('wins_against') else initial_set()
#         self.avg_win_time = kwargs['avg_win_time'] if kwargs.get('avg_win_time') else initial_set()
#         self.avg_loss_time = kwargs['avg_loss_time'] if kwargs.get('avg_loss_time') else initial_set()
#
#     def mutate(self):
#         # mutation rate is 50%
#         values = self.__dict__.copy()
#         for field, value in values.items():
#             if random.randint(0, 1):
#                 values.update({field: random.uniform(self.__getattribute__(field) - self.DEVIATION,
#                                                      self.__getattribute__(field) + self.DEVIATION)})
#         return Chromosome.objects.create(**values)
