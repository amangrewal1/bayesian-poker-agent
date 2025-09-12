"""Belief is always normalized"""

import numpy as np
from agents import BayesianAgent


def test_initial_belief_normalized():
    a = BayesianAgent()
    info = {"hole": ((0, 0), (0, 1)), "community": [], "opponent_id": 1,
            "history": [], "current_bet": 0, "contributions": [1, 2],
            "player": 0, "street": 0}
    b = a._belief(info)
    assert abs(b.sum() - 1.0) < 1e-9

