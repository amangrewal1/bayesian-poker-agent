from poker import Card, hand_strength


def test_pair_in_hole_preflop_range():
    # Pocket deuces preflop — should be a finite equity in (0, 1)
    hole = [Card(0, 0), Card(0, 1)]  # 2-clubs, 2-diamonds
    community = []
    s = hand_strength(hole, community)
    assert 0.0 <= s <= 1.0


def test_pocket_aces_preflop_strongest_hand():
    # Pocket aces preflop should be stronger than pocket twos
    aces = [Card(12, 2), Card(12, 3)]  # A-hearts, A-spades
    deuces = [Card(0, 0), Card(0, 1)]
    s_aces = hand_strength(aces, [])
    s_deuces = hand_strength(deuces, [])
    assert s_aces > s_deuces
