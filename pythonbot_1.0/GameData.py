import HandRankings as Hand


class GameData:
    def __init__(self, name, opponent_name, bb=2):
        # match stats
        self.name = name
        self.opponent_name = opponent_name
        self.num_hands = 0
        self.num_wins = 0
        self.num_flop = 0
        self.big_blind = bb
        # self pre-flop stats
        self.num_self_pfr = 0
        self.num_self_three_bet = 0
        # opponent pre-flop stats
        self.num_pfr = 0
        self.num_vpip = 0
        self.num_pre_fold = 0
        self.num_three_bet = 0
        self.num_fold_pfr = 0
        self.num_fold_three_bet = 0
        # self post-flop stats
        self.aggression_factor = 0.0
        self.num_self_showdown = 0
        self.num_self_c_bet = 0
        self.num_self_showdown_win = 0
        self.num_self_double_barrel = 0
        # opponent post-flop stats
        self.num_raise = 0
        self.num_bet = 0
        self.num_call = 0
        self.num_showdown = 0
        self.num_c_bet = 0
        self.num_fold_c_bet = 0
        self.num_double_barrel = 0
        # current hand stats
        self.button = True
        self.current_pot_size = 0
        self.current_hand = []
        self.current_hand_strength = 0.0
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

    def new_hand(self, data_list):
        self.num_hands += 1
        self.button = data_list[2]
        self.current_hand = [data_list[3], data_list[4]]
        self.current_hand_strength = Hand.hand_win_odds(self.current_hand)
        self.current_game_state = 'PREFLOP'
        self.board_cards = []
        self.last_actions = []
        self.current_legal_actions = []

    def get_action(self, data_list):
        self.current_pot_size = data_list[1]

        num_board_cards = int(data_list[2])
        for i in range(num_board_cards):
            self.board_cards.append(data_list[3 + i])

        index = 3 + num_board_cards
        num_last_actions = int(data_list[index])
        index += 1
        current_last_actions = []
        for i in range(num_last_actions):
            current_last_actions.append(data_list[index + i])

        if self.current_pot_size == 4:
            if self.button:
                self.has_called = True
            else:
                self.opponent_has_called = True
        else:
            for action in self.current_last_actions:
                pass  # record stats

        index += num_last_actions
        num_legal_actions = int(data_list[index])
        index += 1
        self.current_legal_actions = []
        for i in range(num_legal_actions):
            self.current_legal_actions.append(data_list[index + i])

    def hand_over(self, data_list):
        num_board_cards = data_list[3]
        index = 4+num_board_cards
        num_last_actions = data_list[index]
        current_last_actions = []
        for i in range(num_last_actions):
            current_last_actions.append(data_list[index+i])
        for action in current_last_actions:
            if 'WIN' in action and self.name in action:
                self.num_wins += 1