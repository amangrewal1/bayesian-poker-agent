"""Bluff frequency estimator updates"""

from agents import BayesianAgent


def test_bluff_freq_initialized():
    a = BayesianAgent()
    assert 0.0 < a.bluff_freq() < 1.0


def test_bluff_freq_is_fraction():
    a = BayesianAgent()
    f = a.bluff_freq()
    assert 0.0 <= f <= 1.0

