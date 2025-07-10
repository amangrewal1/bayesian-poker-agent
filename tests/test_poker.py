from poker import hand_strength


def test_hand_strength_in_range():
    s = hand_strength(((0, 12), (1, 12)), [])  # paired aces preflop
    assert 0.0 <= s <= 1.0
