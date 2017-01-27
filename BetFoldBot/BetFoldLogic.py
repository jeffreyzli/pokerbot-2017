from DiscardLogicSimple import discard_logic_post_flop, discard_logic_post_turn


def pre_flop_hand_eval(my_hand):
    hand_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                   'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    card_one_value = hand_values[my_hand[0][0]]
    card_one_suit = my_hand[0][1]
    card_two_value = hand_values[my_hand[1][0]]
    card_two_suit = my_hand[1][1]

    if card_one_value == card_two_value:
        if card_one_value > 4:
            return True
        return False
    same_suit = card_one_suit is card_two_suit
    card_min_value = min(card_one_value, card_two_value)
    card_max_value = max(card_one_value, card_two_value)
    if card_max_value == 14:
        return True
    elif card_max_value == 13:
        return card_min_value > 5 or same_suit and card_min_value > 2
    elif card_max_value == 12:
        return card_min_value > 8 or same_suit and card_min_value > 5
    elif card_max_value == 11:
        return card_min_value > 9 or same_suit and card_min_value > 7


def action(game_data):

    if game_data.current_game_state is 'PREFLOP':
        if pre_flop_hand_eval(game_data.current_hand):
            limits = game_data.legal_action('RAISE')
            if limits is not None:
                return 'RAISE:' + str(limits[1])
            return 'CALL'
        elif game_data.current_hand_strength > 0.55:
            limits = game_data.legal_action('CALL')
            if limits is not None:
                return 'CALL'
        limits = game_data.legal_action('CHECK')
        if limits:
            return 'CHECK'
        return 'FOLD'
    if game_data.discard:
        if game_data.current_game_state is 'FLOPTURN':
            discard, card = discard_logic_post_flop(game_data.current_hand, game_data.board_cards)
            if discard:
                game_data.discarded_card = card
                return 'DISCARD:' + card
        elif game_data.current_game_state is 'TURNRIVER':
            discard, card = discard_logic_post_turn(game_data.current_hand, game_data.board_cards,
                                                    game_data.discarded_card)
            if discard:
                return 'DISCARD:' + card
        game_data.discard = False
    if 'High Card' in game_data.hand_class or 'Pair' in game_data.hand_class and 'Two Pair' not in game_data.hand_class:
        limits = game_data.legal_action('CHECK')
        if limits:
            return 'CHECK'
        else:
            return 'FOLD'
    else:
        if game_data.current_game_state is 'POSTRIVER':
            limits = game_data.legal_action('BET')
            if limits is not None:
                return 'BET:' + str(limits[1])
            limits = game_data.legal_action('RAISE')
            if limits is not None:
                return 'RAISE:' + str(limits[1])
        limits = game_data.legal_action('CALL')
        if limits is not None:
            return 'CALL'
        return 'CHECK'
