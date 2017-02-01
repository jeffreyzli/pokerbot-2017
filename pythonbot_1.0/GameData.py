import HandRankings as Hand
from deuces.deuces import Card, Evaluator


class GameData:
    def __init__(self, name, opponent_name, stack_size, bb):
        self.deck = ['2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s',
                     '6c', '6d',
                     '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Tc', 'Td',
                     'Th', 'Ts',
                     'Jc', 'Jd', 'Jh', 'Js', 'Qc', 'Qd', 'Qh', 'Qs', 'Kc', 'Kd', 'Kh', 'Ks', 'Ac', 'Ad', 'Ah', 'As']
        # match stats
        self.name = name
        self.opponent_name = opponent_name
        self.starting_stack_size = int(stack_size)
        self.num_hands = 0
        self.num_wins = 0
        self.num_flop = 0
        self.big_blind = int(bb)
        # self pre-flop stats
        self.pfr = 0
        self.vpip = 0
        self.three_bet = 0
        self.fold_big_bet = 0
        # opponent pre-flop stats
        self.opponent_pfr = 0
        self.opponent_vpip = 0
        self.opponent_three_bet = 0
        self.opponent_fold_pfr = 0
        self.opponent_fold_three_bet = 0
        # self post-flop stats
        self.aggression_factor = False
        self.showdown = 0
        self.c_bet = 0
        self.showdown_win = 0
        self.double_barrel = 0
        self.discarded_card = None
        # opponent post-flop stats
        self.opponent_c_bet = 0
        self.opponent_fold_c_bet = 0
        self.opponent_double_barrel = 0
        # current hand stats
        self.button = True
        self.current_pot_size = 0
        self.current_hand = []
        self.current_hand_strength = 0.0
        self.hand_class = ''
        self.hand_score = 0
        self.current_game_state = ''
        self.board_cards = []
        self.last_actions = []
        self.current_legal_actions = []
        self.has_called = False
        self.opponent_has_called = False
        self.has_two_bet = False
        self.opponent_has_two_bet = False
        self.has_three_bet = False
        self.opponent_has_three_bet = False
        self.has_four_bet = False
        self.opponent_has_four_bet = False
        self.street_dict = {'0': 0, '3': 0, '4': 0, '5': 0}
        self.discard = False
        self.has_five_bet = False
        self.has_bet_aggressively = False
        self.time_bank = 0.0
        self.opc = 0

    def new_hand(self, data_list):
        self.num_hands += 1
        self.button = data_list[2]
        if "true" in self.button:
            self.button = True
        else:
            self.button = False
        self.current_hand = [data_list[3], data_list[4]]
        self.current_hand_strength = Hand.hand_win_odds(self.current_hand)
        self.current_game_state = 'PREFLOP'
        self.board_cards = []
        self.last_actions = []
        self.current_legal_actions = []
        self.street_dict = {'0': 0, '3': 0, '4': 0, '5': 0}
        self.has_two_bet = False
        self.opponent_has_two_bet = False
        self.has_three_bet = False
        self.opponent_has_three_bet = False
        self.has_four_bet = False
        self.opponent_has_four_bet = False
        self.has_bet_aggressively = False
        self.aggression_factor = False
        self.discarded_card = None

    def get_action(self, data_list):
        self.current_pot_size = int(data_list[1])
        self.opc = self.starting_stack_size - self.current_pot_size
        self.time_bank = float(data_list[-1])

        num_board_cards = int(data_list[2])
        self.street_dict[str(num_board_cards)] += 1
        if self.current_game_state == 'PREFLOP':
            if self.street_dict['3'] > 0 and self.street_dict['4'] == 0:
                self.has_two_bet = False
                self.opponent_has_two_bet = False
                self.has_three_bet = False
                self.opponent_has_three_bet = False
                self.has_four_bet = False
                self.opponent_has_four_bet = False
                self.has_bet_aggressively = False
                self.current_game_state = 'FLOPTURN'
                self.num_flop += 1
        elif self.current_game_state == 'FLOPTURN':
            if self.street_dict['4'] > 0 and self.street_dict['5'] == 0:
                self.has_two_bet = False
                self.opponent_has_two_bet = False
                self.has_three_bet = False
                self.opponent_has_three_bet = False
                self.has_four_bet = False
                self.opponent_has_four_bet = False
                self.has_bet_aggressively = False
                self.current_game_state = 'TURNRIVER'
        elif self.current_game_state == 'TURNRIVER':
            if self.street_dict['5'] > 0:
                self.has_two_bet = False
                self.opponent_has_two_bet = False
                self.has_three_bet = False
                self.opponent_has_three_bet = False
                self.has_four_bet = False
                self.opponent_has_four_bet = False
                self.has_bet_aggressively = False
                self.current_game_state = 'POSTRIVER'
        for i in range(num_board_cards):
            board_card = data_list[3 + i]
            if board_card not in self.board_cards:
                self.board_cards.append(data_list[3 + i])
        if num_board_cards > 0:
            board_cards = []
            for board_card in self.board_cards:
                board_cards.append(Card.new(board_card))
            hand = []
            for card in self.current_hand:
                hand.append(Card.new(card))
            self.hand_score = Evaluator().evaluate(hand, board_cards)
            self.hand_class = Evaluator().class_to_string(Evaluator().get_rank_class(self.hand_score))

        index = 3 + num_board_cards
        num_last_actions = int(data_list[index])
        index += 1
        current_last_actions = []
        for i in range(num_last_actions):
            current_last_actions.append(data_list[index + i])
        self.last_actions.append(current_last_actions)

        if self.discard:
            for action in current_last_actions:
                if 'DISCARD' in action and self.name in action:
                    old_card = action[8:10]
                    new_card = action[11:13]
                    self.current_hand[self.current_hand.index(old_card)] = new_card
                    self.current_hand_strength = Hand.hand_win_odds(self.current_hand)
                    self.discard = False
                    break

        if self.current_game_state == 'PREFLOP':
            if self.current_pot_size == 4:
                if self.button:
                    self.vpip += 1
                    self.has_called = True
                else:
                    self.opponent_vpip += 1
                    self.opponent_has_called = True
            else:
                for action in current_last_actions:
                    if 'RAISE' in action:
                        round_num = self.street_dict['0']
                        if round_num == 1:
                            self.opponent_pfr += 1
                            self.opponent_vpip += 1
                            self.opponent_has_two_bet = True
                        elif round_num == 2:
                            if self.button:
                                if self.name in action:
                                    self.pfr += 1
                                    self.vpip += 1
                                    self.has_two_bet = True
                                else:
                                    self.opponent_pfr += 1
                                    self.opponent_vpip += 1
                                    self.opponent_has_three_bet = True
                            else:
                                if self.name in action:
                                    self.pfr += 1
                                    self.vpip += 1
                                    self.has_three_bet = True
                                else:
                                    self.opponent_pfr += 1
                                    self.opponent_vpip += 1
                                    self.opponent_has_four_bet = True
                        elif round_num == 3:
                            if self.name in action:
                                self.pfr += 1
                                self.vpip += 1
                    elif 'CALL' in action:
                        if self.name in action:
                            self.vpip += 1
                        else:
                            self.opponent_vpip += 1
        elif self.current_game_state == 'FLOPTURN':
            round_num = self.street_dict['3']
            if round_num == 1:
                self.discard = True
            elif round_num == 2:
                for action in current_last_actions:
                    if 'BET' in action:
                        self.opponent_c_bet += 1
                        break
            elif round_num == 3:
                for action in current_last_actions:
                    if 'BET' in action:
                        if self.name in action:
                            self.c_bet += 1
                        else:
                            self.opponent_c_bet += 1
                    elif 'RAISE' in action:
                        if self.name in action:
                            self.has_two_bet = True
                        else:
                            if self.button:
                                self.opponent_has_three_bet = True
                            else:
                                self.opponent_has_two_bet = True
            elif round_num == 4:
                for action in current_last_actions:
                    if 'RAISE' in action:
                        if self.name in action:
                            if self.button:
                                self.has_four_bet = True
                            else:
                                self.has_three_bet = True
                        break
        elif self.current_game_state == 'TURNRIVER':
            round_num = self.street_dict['4']
            if round_num == 1:
                self.discard = True
                for action in current_last_actions:
                    if 'BET' in action:
                        if self.name in action:
                            self.c_bet += 1
                        else:
                            self.opponent_c_bet += 1
                        break
            elif round_num == 2:
                for action in current_last_actions:
                    if 'BET' in action:
                        self.opponent_c_bet += 1
                        break
            elif round_num == 3:
                for action in current_last_actions:
                    if 'BET' in action:
                        if self.name in action:
                            self.c_bet += 1
                        else:
                            self.opponent_c_bet += 1
                    elif 'RAISE' in action:
                        if self.name in action:
                            self.has_two_bet = True
                        else:
                            if self.button:
                                self.opponent_has_three_bet = True
                            else:
                                self.opponent_has_two_bet = True
            elif round_num == 4:
                for action in current_last_actions:
                    if 'RAISE' in action:
                        if self.name in action:
                            if self.button:
                                self.has_four_bet = True
                            else:
                                self.has_three_bet = True
                        break
        elif self.current_game_state == 'POSTRIVER':
            round_num = self.street_dict['5']
            if round_num == 1:
                for action in current_last_actions:
                    if 'BET' in action:
                        if self.name in action:
                            self.double_barrel += 1
                        else:
                            self.opponent_double_barrel += 1
                        break

        index += num_last_actions
        num_legal_actions = int(data_list[index])
        index += 1
        self.current_legal_actions = []
        for i in range(num_legal_actions):
            self.current_legal_actions.append(data_list[index + i])

    def legal_action(self, action):
        for legal_action in self.current_legal_actions:
            if action in legal_action:
                if action == 'BET' or action == 'RAISE':
                    index = legal_action.index(':') + 1
                    sub = legal_action[index:]
                    index = sub.index(':')
                    return [int(sub[:index]), int(sub[index + 1:])]
                if action == 'CALL':
                    for last_action in self.last_actions[-1]:
                        if 'RAISE' in last_action and self.opponent_name in last_action:
                            sub = last_action[last_action.index(':') + 1:]
                            return int(sub[:sub.index(':')])
                return True
        return None

    def hand_over(self, data_list):
        num_board_cards = data_list[3]
        index = 4 + num_board_cards
        num_last_actions = data_list[index]
        current_last_actions = []
        for i in range(num_last_actions):
            current_last_actions.append(data_list[index + i])
        if self.current_game_state == 'PREFLOP':
            for action in current_last_actions:
                if 'FOLD' in action and self.opponent_name in action:
                    if self.button:
                        for last_action in self.last_actions[-1]:
                            if 'RAISE' in last_action and self.name in last_action:
                                self.opponent_fold_pfr += 1
                                if self.has_three_bet and not self.has_four_bet:
                                    self.opponent_fold_three_bet += 1
                        self.num_wins += 1
                    else:
                        for last_action in current_last_actions:
                            if 'RAISE' in last_action and self.name in last_action:
                                self.opponent_fold_pfr += 1
                                if self.has_three_bet and not self.has_four_bet:
                                    self.opponent_fold_three_bet += 1
                        self.num_wins += 1
        elif self.current_game_state == 'FLOPTURN':
            for action in current_last_actions:
                if self.button:
                    if 'FOLD' in action and self.opponent_name in action:
                        for last_action in self.last_actions[-1]:
                            if 'BET' in last_action and self.name in last_action:
                                self.opponent_fold_c_bet += 1
                    self.num_wins += 1
                else:
                    if 'FOLD' in action and self.opponent_name in action:
                        for last_action in current_last_actions:
                            if 'BET' in last_action and self.name in last_action:
                                self.opponent_fold_c_bet += 1
                    self.num_wins += 1

        elif self.current_game_state == 'POSTRIVER':
            for action in current_last_actions:
                if 'WIN' in action:
                    if self.name in action:
                        self.num_wins += 1
                    for last_action in current_last_actions:
                        if 'SHOW' in last_action:
                            self.showdown += 1
                            self.showdown_win += 1
                            break
                    break
