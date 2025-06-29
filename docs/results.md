# Interpreting the Results

The Bayesian agent's **hand-count win rate** (39%) is lower than the
symmetric-threshold baseline (48%). This looks surprising, but it is the
signature of correct poker strategy: folding marginal hands against strong
opponent action.

The meaningful metric is **big blinds per 100 hands (bb/100)**:
- Baseline vs itself: ~0 bb/100 (symmetric, zero sum)
- Bayesian vs Baseline: **+50.8 bb/100** over 50k hands

At showdown, the Bayesian agent wins 24% more often than the baseline does,
because it has already folded its weakest hands preflop.
