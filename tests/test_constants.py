"""Game constants are defined"""

from game import FOLD, CHECK_CALL, BET_RAISE, BET_SIZE_PRE, BET_SIZE_POST


def test_actions_distinct():
    assert FOLD != CHECK_CALL != BET_RAISE


def test_bet_sizes_positive():
    assert BET_SIZE_PRE > 0
    assert BET_SIZE_POST > 0

