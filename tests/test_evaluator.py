from poker import hand_strength


def test_royal_flush_strong():
    # A, K, Q, J, 10 of hearts -> royal flush
    hole = ((2, 12), (2, 11))  # A-hearts, K-hearts
    community = [(2, 10), (2, 9), (2, 8)]  # Q-hearts, J-hearts, 10-hearts
    assert hand_strength(hole, community) > 0.95


def test_pair_of_deuces_weak():
    # Pocket deuces preflop, weakish
    hole = ((0, 0), (1, 0))  # 2-clubs, 2-diamonds
    community = []
    s = hand_strength(hole, community)
    assert 0.4 < s < 0.7
