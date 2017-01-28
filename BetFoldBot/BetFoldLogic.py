from DiscardLogicSimple import discard_logic_post_flop, discard_logic_post_turn


def pre_flop_hand_eval(my_hand, hand_strength):
    hand_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                   'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    card_one_value = hand_values[my_hand[0][0]]
    card_one_suit = my_hand[0][1]
    card_two_value = hand_values[my_hand[1][0]]
    card_two_suit = my_hand[1][1]

    if hand_strength > 0.65:
        return False

    if card_one_value == card_two_value:
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

    # returns whether we want to go all-in PreFlop


def action(game_data):

    if game_data.current_game_state is 'PREFLOP':
        if pre_flop_hand_eval(game_data.current_hand, game_data.current_hand_strength):
            limits = game_data.legal_action('RAISE')
            if limits is not None:
                game_data.current_stack_size = game_data.starting_stack_size - limits[1]     # update current stack size
                return 'RAISE:' + str(limits[1])
            limits = game_data.legal_action('CALL')
            game_data.current_stack_size = game_data.starting_stack_size - limits            # update current stack size
            return 'CALL'
    # elif our hand is a pair AND > 0.55, or our hand is > 0.70, play call-check. We want bet limit else > 0.55.
        elif game_data.current_hand_strength > 0.55:
            bet_limit = game_data.starting_stack_size  # no bet_limit, play Call Check
            if game_data.current_hand_strength < 0.65:  # if not pair
                bet_limit = 55  # bet_limit of 55
            limits = game_data.legal_action('CALL')
            if limits is not None and (game_data.current_pot_size - game_data.opc < bet_limit):
                game_data.current_stack_size = game_data.starting_stack_size - limits   # update current stack size
                return 'CALL'
        if game_data.current_pot_size == 3:
            game_data.current_stack_size -= game_data.big_blind
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
    if 'High' in game_data.hand_class or 'Pair' in game_data.hand_class and 'Two' not in game_data.hand_class:
        limits = game_data.legal_action('CHECK')
        if limits:
            return 'CHECK'
        else:
            return 'FOLD'
    else:
        if game_data.current_game_state is 'POSTRIVER':
            limits = game_data.legal_action('BET')
            if limits is not None:
                if game_data.hand_score < game_data.board_score:
                    game_data.current_pot_size = game_data.starting_stack_size - limits[1]  # update current stack size
                    return 'BET:' + str(limits[1])
            limits = game_data.legal_action('RAISE')
            if limits is not None:
                if game_data.hand_score < game_data.board_score:
                    game_data.current_pot_size = game_data.starting_stack_size - limits[1]  # update current stack size
                    return 'RAISE:' + str(limits[1])
        limits = game_data.legal_action('CALL')
        if limits is not None:
            if game_data.hand_score < game_data.board_score:
                game_data.current_pot_size = game_data.starting_stack_size - limits             # update current stack size
                return 'CALL'
        return 'CHECK'
