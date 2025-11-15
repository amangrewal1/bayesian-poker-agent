# Showdown Tiebreaks

When two hands have the same 5-card ranking (e.g. both two-pair), the
tiebreak is resolved by the sorted tuple of ranks within the hand class:
- Two-pair: (high_pair, low_pair, kicker)
- One-pair: (pair, k1, k2, k3)
- High card: (r1, r2, r3, r4, r5) descending

The 7-card evaluator returns the canonical sort key for ties.
