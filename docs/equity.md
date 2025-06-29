# Hand-Strength Equity

Preflop equity for each of the 169 canonical starting hands is precomputed
by Monte Carlo simulation against a uniform random opponent. The table is
cached to disk on first run (~7 seconds).

Postflop, hand strength is computed directly from the 7-card evaluator over
the hole + community cards. The evaluator returns a normalized [0, 1] score
where 1.0 is a royal flush and 0.0 is a 7-high no-pair.
