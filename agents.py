import random
import numpy as np
from poker import hand_strength
from game import FOLD, CHECK_CALL, BET_RAISE, BET_SIZE_PRE, BET_SIZE_POST


class FixedThresholdAgent:
    """Raises/calls/folds based on fixed equity thresholds."""

    def __init__(self, raise_eq=0.58, call_eq=0.32, rng=None):
        self.raise_eq = raise_eq
        self.call_eq = call_eq
        self.rng = rng or random.Random()

    def act(self, info, legal):
        eq = hand_strength(info['hole'], info['community'])
        owe = info['current_bet'] - info['contributions'][info['player']]
        if owe == 0:
            if eq >= self.raise_eq and BET_RAISE in legal:
                return BET_RAISE
            return CHECK_CALL
        if eq >= self.raise_eq and BET_RAISE in legal:
            return BET_RAISE
        if eq >= self.call_eq:
            return CHECK_CALL
        return FOLD

    def observe(self, opp_hole, community, opp_actions):
        pass

    def reset_episode(self):
        pass


class BayesianAgent:
    """Maintains posterior belief over opponent's hand-strength bucket
    from observed betting actions, and updates call thresholds based on
    inferred bluff frequency."""

    def __init__(self, n_buckets=5, rng=None):
        self.n_buckets = n_buckets
        self.rng = rng or random.Random()
        self.action_counts = self._seed_counts()
        self.bluff_raises = 1.0
        self.total_raises = 4.0

    def _seed_counts(self):
        c = np.ones((self.n_buckets, 3)) * 1.0
        for b in range(self.n_buckets):
            c[b, FOLD] += max(0.0, (self.n_buckets - 1 - b) * 4.0)
            c[b, BET_RAISE] += max(0.0, b * 4.0)
            c[b, CHECK_CALL] += 4.0 if b == self.n_buckets // 2 else 2.0
        return c

    def _likelihood(self):
        return self.action_counts / self.action_counts.sum(axis=1, keepdims=True)

    def _belief(self, info):
        lk = self._likelihood()
        belief = np.ones(self.n_buckets) / self.n_buckets
        opp = info['opponent_id']
        for p, _, a in info['history']:
            if p != opp:
                continue
            belief = belief * lk[:, a]
            total = belief.sum()
            belief = belief / total if total > 0 else np.ones(self.n_buckets) / self.n_buckets
        return belief

    def bluff_freq(self):
        return self.bluff_raises / self.total_raises

    def _win_prob(self, my_strength, belief):
        total = 0.0
        for b in range(self.n_buckets):
            lo = b / self.n_buckets
            hi = (b + 1) / self.n_buckets
            if my_strength >= hi:
                p = 1.0
            elif my_strength < lo:
                p = 0.0
            else:
                p = (my_strength - lo) / (hi - lo)
            total += belief[b] * p
        return total

    def act(self, info, legal):
        my_strength = hand_strength(info['hole'], info['community'])
        belief = self._belief(info)
        win_p = self._win_prob(my_strength, belief)

        pot = sum(info['contributions'])
        owe = info['current_bet'] - info['contributions'][info['player']]
        bet_size = BET_SIZE_PRE if info['street'] == 0 else BET_SIZE_POST
        pot_odds = owe / (pot + owe) if owe > 0 else 0.0
        bluff = self.bluff_freq()

        lk = self._likelihood()
        p_opp_fold_to_bet = float(np.sum(belief * lk[:, FOLD]))

        call_thresh = max(0.10, pot_odds - 0.35 * bluff)

        if owe == 0:
            if win_p >= 0.55 and BET_RAISE in legal:
                return BET_RAISE
            if p_opp_fold_to_bet >= 0.30 and BET_RAISE in legal:
                return BET_RAISE
            return CHECK_CALL

        if win_p >= 0.68 and BET_RAISE in legal:
            return BET_RAISE
        if win_p < call_thresh and p_opp_fold_to_bet >= 0.55 and BET_RAISE in legal:
            return BET_RAISE
        if win_p >= call_thresh:
            return CHECK_CALL
        return FOLD

    def observe(self, opp_hole, community, opp_actions):
        if opp_hole is None:
            return
        opp_strength = hand_strength(opp_hole, community)
        bucket = min(int(opp_strength * self.n_buckets), self.n_buckets - 1)
        for a in opp_actions:
            self.action_counts[bucket, a] += 1
            if a == BET_RAISE:
                self.total_raises += 1
                if bucket <= 1:
                    self.bluff_raises += 1

    def reset_episode(self):
        pass
