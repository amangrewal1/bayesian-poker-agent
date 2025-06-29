# Bayesian Strategy

The Bayesian agent treats opponent hand strength as a hidden categorical variable
over 5 equity buckets. Each observed opponent action multiplies the per-bucket
likelihood into the posterior. Across hands, a Dirichlet likelihood over
(bucket, action) counts is refined using showdown-revealed hands.

Bluff frequency is tracked as a running estimate of `P(weak-hand | raise)`.
When bluff frequency is high, call thresholds are lowered so the agent does
not fold marginal hands to aggressive opponents.
