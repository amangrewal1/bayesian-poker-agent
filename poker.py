from collections import Counter
from itertools import combinations
import random

RANKS = '23456789TJQKA'
SUITS = 'cdhs'


class Card:
    __slots__ = ('rank', 'suit')

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return RANKS[self.rank] + SUITS[self.suit]

    def __eq__(self, o):
        return isinstance(o, Card) and self.rank == o.rank and self.suit == o.suit

    def __hash__(self):
        return self.rank * 4 + self.suit

    def __lt__(self, o):
        return (self.rank, self.suit) < (o.rank, o.suit)


def full_deck():
    return [Card(r, s) for r in range(13) for s in range(4)]


HIGH_CARD, PAIR, TWO_PAIR, TRIPS, STRAIGHT, FLUSH, FULL_HOUSE, QUADS, STRAIGHT_FLUSH = range(9)


def _eval5(cards):
    ranks = sorted((c.rank for c in cards), reverse=True)
    rc = Counter(ranks)
    rc_sorted = sorted(rc.items(), key=lambda x: (-x[1], -x[0]))
    flush = len({c.suit for c in cards}) == 1
    uniq = sorted(set(ranks), reverse=True)
    straight_hi = -1
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            straight_hi = uniq[0]
        elif uniq == [12, 3, 2, 1, 0]:
            straight_hi = 3
    if flush and straight_hi >= 0:
        return (STRAIGHT_FLUSH, straight_hi)
    if rc_sorted[0][1] == 4:
        kicker = next(r for r, c in rc_sorted if c == 1)
        return (QUADS, rc_sorted[0][0], kicker)
    if rc_sorted[0][1] == 3 and rc_sorted[1][1] == 2:
        return (FULL_HOUSE, rc_sorted[0][0], rc_sorted[1][0])
    if flush:
        return (FLUSH, *ranks)
    if straight_hi >= 0:
        return (STRAIGHT, straight_hi)
    if rc_sorted[0][1] == 3:
        kk = sorted((r for r, c in rc_sorted if c == 1), reverse=True)
        return (TRIPS, rc_sorted[0][0], *kk)
    if rc_sorted[0][1] == 2 and rc_sorted[1][1] == 2:
        hp = max(rc_sorted[0][0], rc_sorted[1][0])
        lp = min(rc_sorted[0][0], rc_sorted[1][0])
        kicker = rc_sorted[2][0]
        return (TWO_PAIR, hp, lp, kicker)
    if rc_sorted[0][1] == 2:
        kk = sorted((r for r, c in rc_sorted if c == 1), reverse=True)
        return (PAIR, rc_sorted[0][0], *kk)
    return (HIGH_CARD, *ranks)


def eval_hand(cards):
    if len(cards) == 5:
        return _eval5(cards)
    return max(_eval5(list(combo)) for combo in combinations(cards, 5))


def _canon_hole(hole):
    r1, r2 = sorted((c.rank for c in hole), reverse=True)
    if r1 == r2:
        return (r1, r2, 0)
    return (r1, r2, 1 if hole[0].suit == hole[1].suit else 2)


_PREFLOP_CACHE = {}


def _mc_preflop_equity(hole, n_samples=400):
    rng = random.Random(hash(_canon_hole(hole)) & 0xFFFFFFFF)
    deck = full_deck()
    hole_set = set(hole)
    remaining = [c for c in deck if c not in hole_set]
    wins = ties = 0
    for _ in range(n_samples):
        draw = rng.sample(remaining, 7)
        opp = draw[:2]
        comm = draw[2:7]
        m = eval_hand(hole + comm)
        o = eval_hand(opp + comm)
        if m > o:
            wins += 1
        elif m == o:
            ties += 1
    return (wins + 0.5 * ties) / n_samples


def preflop_strength(hole):
    key = _canon_hole(hole)
    if key not in _PREFLOP_CACHE:
        _PREFLOP_CACHE[key] = _mc_preflop_equity(hole)
    return _PREFLOP_CACHE[key]


_STRENGTH_RANGES = [
    (0.05, 0.28),
    (0.30, 0.68),
    (0.70, 0.85),
    (0.85, 0.92),
    (0.90, 0.95),
    (0.93, 0.96),
    (0.96, 0.98),
    (0.98, 0.99),
    (0.99, 1.00),
]


def postflop_strength(hole, community):
    hand = eval_hand(hole + community)
    cat = hand[0]
    lo, hi = _STRENGTH_RANGES[cat]
    if len(hand) > 1:
        primary = hand[1]
        return lo + (primary / 12) * (hi - lo)
    return (lo + hi) / 2


def hand_strength(hole, community):
    if not community:
        return preflop_strength(hole)
    return postflop_strength(hole, community)


def precompute_preflop():
    for r1 in range(13):
        for r2 in range(r1 + 1):
            if r1 == r2:
                preflop_strength([Card(r1, 0), Card(r1, 1)])
            else:
                preflop_strength([Card(r1, 0), Card(r2, 0)])
                preflop_strength([Card(r1, 0), Card(r2, 1)])
