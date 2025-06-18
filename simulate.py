import random
from game import GameState


def run_hand(agent0, agent1, rng, button=0):
    game = GameState(rng=rng)
    game.reset(button=button)
    agent0.reset_episode()
    agent1.reset_episode()

    opp_actions = {0: [], 1: []}

    while not game.finished:
        player = game.to_act
        info = game.info_for(player)
        legal = game.legal_actions(player)
        agent = agent0 if player == 0 else agent1
        action = agent.act(info, legal)
        if action not in legal:
            action = legal[0]
        game.apply(action)
        opp_actions[1 - player].append(action)

    showdown = game.folded is None
    if showdown:
        agent0.observe(game.holes[1], game.community, opp_actions[0])
        agent1.observe(game.holes[0], game.community, opp_actions[1])
    else:
        agent0.observe(None, game.community, opp_actions[0])
        agent1.observe(None, game.community, opp_actions[1])

    return game.result()


def run_hand_detailed(agent0, agent1, rng, button=0):
    from game import GameState, FOLD
    game = GameState(rng=rng)
    game.reset(button=button)
    agent0.reset_episode()
    agent1.reset_episode()
    opp_actions = {0: [], 1: []}
    while not game.finished:
        player = game.to_act
        info = game.info_for(player)
        legal = game.legal_actions(player)
        agent = agent0 if player == 0 else agent1
        action = agent.act(info, legal)
        if action not in legal:
            action = legal[0]
        game.apply(action)
        opp_actions[1 - player].append(action)
    showdown = game.folded is None
    if showdown:
        agent0.observe(game.holes[1], game.community, opp_actions[0])
        agent1.observe(game.holes[0], game.community, opp_actions[1])
    else:
        agent0.observe(None, game.community, opp_actions[0])
        agent1.observe(None, game.community, opp_actions[1])
    return game.result(), showdown, game.folded


def simulate(n_hands, agent0, agent1, seed=0, verbose=False, report_every=5000):
    rng = random.Random(seed)
    p0_total = p1_total = 0
    p0_wins = p1_wins = ties = 0
    showdowns = 0
    p0_sd_wins = p1_sd_wins = 0
    p0_forced_folds = p1_forced_folds = 0

    for i in range(n_hands):
        button = i % 2
        (r0, r1), showdown, folded = run_hand_detailed(agent0, agent1, rng, button=button)
        p0_total += r0
        p1_total += r1
        if r0 > 0:
            p0_wins += 1
        elif r1 > 0:
            p1_wins += 1
        else:
            ties += 1
        if showdown:
            showdowns += 1
            if r0 > 0:
                p0_sd_wins += 1
            elif r1 > 0:
                p1_sd_wins += 1
        else:
            if folded == 1:
                p0_forced_folds += 1
            else:
                p1_forced_folds += 1

        if verbose and (i + 1) % report_every == 0:
            print(f"  hand {i+1:>6}/{n_hands}: p0_winrate={p0_wins/(i+1):.3f} "
                  f"p0_bb/hand={p0_total/(i+1):+.3f}")

    return {
        'p0_chips': p0_total,
        'p1_chips': p1_total,
        'p0_winrate': p0_wins / n_hands,
        'p1_winrate': p1_wins / n_hands,
        'tie_rate': ties / n_hands,
        'p0_bb_per_hand': p0_total / n_hands,
        'p1_bb_per_hand': p1_total / n_hands,
        'showdowns': showdowns,
        'p0_sd_winrate': p0_sd_wins / max(1, showdowns),
        'p1_sd_winrate': p1_sd_wins / max(1, showdowns),
        'p0_forced_folds': p0_forced_folds,
        'p1_forced_folds': p1_forced_folds,
        'n_hands': n_hands,
    }
