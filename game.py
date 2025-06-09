import random
from poker import full_deck, eval_hand

FOLD, CHECK_CALL, BET_RAISE = 0, 1, 2
ACTION_NAMES = {FOLD: 'fold', CHECK_CALL: 'check/call', BET_RAISE: 'bet/raise'}

SB, BB = 1, 2
BET_SIZE_PRE, BET_SIZE_POST = 2, 4
MAX_RAISES = 3


class GameState:
    def __init__(self, rng=None):
        self.rng = rng or random.Random()
        self.reset()

    def reset(self, button=0):
        deck = full_deck()
        self.rng.shuffle(deck)
        self.holes = [deck[:2], deck[2:4]]
        self.community = deck[4:9]
        self.button = button
        self.street = 0
        self.contributions = [0, 0]
        self.contributions[button] = SB
        self.contributions[1 - button] = BB
        self.current_bet = BB
        self.raises_this_street = 1
        self.to_act = button
        self.finished = False
        self.folded = None
        self.winner = None
        self.action_history = []

    def legal_actions(self, player):
        if self.finished or player != self.to_act:
            return []
        owe = self.current_bet - self.contributions[player]
        actions = []
        if owe > 0:
            actions.append(FOLD)
            actions.append(CHECK_CALL)
        else:
            actions.append(CHECK_CALL)
        if self.raises_this_street < MAX_RAISES:
            actions.append(BET_RAISE)
        return actions

    def apply(self, action):
        player = self.to_act
        self.action_history.append((player, self.street, action))

        if action == FOLD:
            self.finished = True
            self.folded = player
            self.winner = 1 - player
            return

        if action == BET_RAISE:
            bet_size = BET_SIZE_PRE if self.street == 0 else BET_SIZE_POST
            self.contributions[player] = self.current_bet + bet_size
            self.current_bet = self.contributions[player]
            self.raises_this_street += 1
            self.to_act = 1 - player
            return

        owe = self.current_bet - self.contributions[player]
        if owe > 0:
            self.contributions[player] = self.current_bet
            if self.street == 0 and self.raises_this_street == 1 and player == self.button:
                self.to_act = 1 - player
            else:
                self._advance_street()
        else:
            opp_acted = any(p != player and s == self.street
                            for p, s, _ in self.action_history[:-1])
            if opp_acted:
                self._advance_street()
            else:
                self.to_act = 1 - player

    def _advance_street(self):
        if self.street == 0:
            self.street = 1
            self.raises_this_street = 0
            self.to_act = 1 - self.button
        else:
            self.finished = True
            self._showdown()

    def _showdown(self):
        h0 = eval_hand(self.holes[0] + self.community)
        h1 = eval_hand(self.holes[1] + self.community)
        if h0 > h1:
            self.winner = 0
        elif h0 < h1:
            self.winner = 1
        else:
            self.winner = -1

    def pot(self):
        return sum(self.contributions)

    def result(self):
        if self.winner == -1:
            return (0, 0)
        if self.winner == 0:
            return (self.contributions[1], -self.contributions[1])
        return (-self.contributions[0], self.contributions[0])

    def info_for(self, player):
        return {
            'hole': self.holes[player],
            'community': self.community if self.street >= 1 else [],
            'street': self.street,
            'contributions': self.contributions[:],
            'current_bet': self.current_bet,
            'raises_this_street': self.raises_this_street,
            'to_act': self.to_act,
            'button': self.button,
            'player': player,
            'opponent_id': 1 - player,
            'history': self.action_history[:],
        }
