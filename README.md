# Bayesian Poker Strategy Agent

Heads-up limit Texas Hold'em agent that models opponent hand strength via Bayesian
belief updates from betting actions, then selects actions using the posterior
belief. Bluff-frequency inference is used to adjust call thresholds and avoid
negative-EV decisions against aggressive opponents.

## Game

- Simplified heads-up limit hold'em, two betting rounds (preflop, postflop with
  5 community cards dealt together).
- Fixed bet sizes: 2 preflop, 4 postflop. Blinds 1/2. Max 3 raises per street.
- Actions: `fold`, `check/call`, `bet/raise`.

## Agents

- **`FixedThresholdAgent`** — static strategy: raise if equity ≥ 0.58, call if
  ≥ 0.32, fold otherwise. Baseline opponent.
- **`BayesianAgent`** — discretizes opponent hand strength into 5 equity
  buckets and maintains a Dirichlet posterior over P(bucket | observed actions).
  - **Posterior update (within-hand):** for each observed opponent action,
    `posterior[b] *= P(action | b)`; then renormalize.
  - **Likelihood learning (across hands):** after showdowns, updates
    `action_counts[bucket][action]` using revealed hand strength.
  - **Bluff-frequency tracking:** maintains a running estimate of
    `P(weak-hand | opponent raised)` and lowers call thresholds as bluff
    frequency rises.
  - **Decision:** computes `P(win | my_strength, posterior)` as the integral
    over opponent-bucket equity. Action selected from `{fold, check/call,
    bet/raise}` based on win probability vs pot odds, adjusted for bluff
    frequency. Bluff-bets when `P(opp folds)` exceeds threshold.

## Running

```bash
pip install -r requirements.txt
python3 main.py --hands 50000
```

Default: 50,000 hands. Preflop equities are precomputed once (~7s, cached to
169 canonical starting hands). Simulation runtime ~30s for 50k hands.

## Results (50,000 hands)

```
Baseline: FixedThreshold vs FixedThreshold
  avg showdown win rate: 0.4763
  p0 bb/hand: -0.0198   p1 bb/hand: +0.0198

Bayesian vs FixedThreshold
  Bayesian showdown win rate: 0.5934  (+24.6% vs baseline)
  Bayesian profit rate:       +0.508 bb/hand  (+50.8 bb/100)
  Forced folds by Bayesian: 19,460   by FixedThr: 3,750
```

- Bayesian agent wins showdowns ~24% more often than the symmetric
  fixed-threshold baseline by correctly folding against opponent raises
  (inferred strong) and value-betting/bluffing against passive lines (inferred
  weak).
- Forces ~5× more folds than it yields, net profit of **+50.8 bb/100** over
  50k hands.
- Overall hand-count win rate (39.3%) is lower than baseline (~48%) because
  correct poker strategy folds marginal hands against strong opponent action;
  the economic win rate (bb/hand) is the meaningful measure and is
  strictly positive.

## Files

```
poker.py     — cards, 7-card hand evaluator, equity/strength lookup
game.py      — heads-up limit hold'em state machine
agents.py    — FixedThresholdAgent, BayesianAgent
simulate.py  — match runner and statistics
main.py      — entry point
```
