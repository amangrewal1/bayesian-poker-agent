from poker import Card, hand_strength


def test_hand_strength_in_range():
    # Paired aces preflop (hearts + spades)
    s = hand_strength([Card(12, 2), Card(12, 3)], [])
    assert 0.0 <= s <= 1.0
