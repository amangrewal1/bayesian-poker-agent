import argparse
import random
import time

from agents import FixedThresholdAgent, BayesianAgent
from simulate import simulate
from poker import precompute_preflop


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hands', type=int, default=50000)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    print("Precomputing preflop equities...")
    t0 = time.time()
    precompute_preflop()
    print(f"  done in {time.time()-t0:.1f}s\n")

    print(f"Baseline: FixedThreshold vs FixedThreshold ({args.hands} hands)")
    base = simulate(
        args.hands,
        FixedThresholdAgent(rng=random.Random(args.seed + 1)),
        FixedThresholdAgent(rng=random.Random(args.seed + 2)),
        seed=args.seed,
        verbose=args.verbose,
    )
    print(f"  avg showdown winrate: {(base['p0_sd_winrate']+base['p1_sd_winrate'])/2:.4f}")
    print(f"  p0 winrate: {base['p0_winrate']:.4f}  sd_winrate: {base['p0_sd_winrate']:.4f}  bb/hand: {base['p0_bb_per_hand']:+.4f}")
    print(f"  p1 winrate: {base['p1_winrate']:.4f}  sd_winrate: {base['p1_sd_winrate']:.4f}  bb/hand: {base['p1_bb_per_hand']:+.4f}")

    print(f"\nBayesian vs FixedThreshold ({args.hands} hands)")
    result = simulate(
        args.hands,
        BayesianAgent(rng=random.Random(args.seed + 3)),
        FixedThresholdAgent(rng=random.Random(args.seed + 4)),
        seed=args.seed + 100,
        verbose=args.verbose,
    )
    print(f"  Bayesian   winrate: {result['p0_winrate']:.4f}  sd_winrate: {result['p0_sd_winrate']:.4f}  bb/hand: {result['p0_bb_per_hand']:+.4f}")
    print(f"  FixedThr.  winrate: {result['p1_winrate']:.4f}  sd_winrate: {result['p1_sd_winrate']:.4f}  bb/hand: {result['p1_bb_per_hand']:+.4f}")
    print(f"  showdowns reached: {result['showdowns']}/{result['n_hands']} "
          f"({result['showdowns']/result['n_hands']*100:.1f}%)")
    print(f"  forced folds by Bayesian: {result['p1_forced_folds']}  "
          f"by FixedThr: {result['p0_forced_folds']}")

    baseline_sd_wr = (base['p0_sd_winrate'] + base['p1_sd_winrate']) / 2
    bayes_sd_wr = result['p0_sd_winrate']
    sd_rel = (bayes_sd_wr - baseline_sd_wr) / baseline_sd_wr * 100

    baseline_bb = (base['p0_bb_per_hand'] - base['p1_bb_per_hand']) / 2
    bayes_bb = result['p0_bb_per_hand']
    print(f"\nResults:")
    print(f"  Bayesian showdown win rate: {bayes_sd_wr:.4f}  vs baseline {baseline_sd_wr:.4f}  (+{sd_rel:.1f}%)")
    print(f"  Bayesian profit rate:       {bayes_bb:+.3f} bb/hand  ({bayes_bb*100:+.1f} bb/100)")


if __name__ == '__main__':
    main()
