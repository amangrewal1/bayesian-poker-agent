# Sample Run

```
$ python3 main.py --hands 10000

Precomputing preflop equity... 7.1s
Baseline: FixedThreshold vs FixedThreshold
  avg showdown win rate: 0.4763
  p0 bb/hand: -0.0198   p1 bb/hand: +0.0198

Bayesian vs FixedThreshold
  Bayesian showdown win rate: 0.5940  (+24.8% vs baseline)
  Bayesian profit rate:       +0.510 bb/hand  (+51.0 bb/100)
  Forced folds by Bayesian: 3,890   by FixedThr: 750
```
