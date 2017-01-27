# from DiscardLogic import discard_logic_post_flop, discard_logic_post_turn
from DiscardLogic56 import discard_logic_post_flop, discard_logic_post_turn
# from DiscardLogicSimple import discard_logic_post_flop, discard_logic_post_turn


def action(game_data):

    if game_data.discard:
        '''if game_data.current_hand_strength <= 0.55:  # WE ARE GOING TO DISCARD
            card_one = game_data.current_hand[0][0]
            card_two = game_data.current_hand[1][0]

            if card_one == 'T':
                card_one = 10
            elif card_one == 'J':
                card_one = 11
            elif card_one == 'Q':
                card_one = 12
            elif card_one == 'K':
                card_one = 13
            elif card_one == 'A':
                card_one = 14
            else:
                card_one = int(card_one)

            if card_two == 'T':
                card_two = 10
            elif card_two == 'J':
                card_two = 11
            elif card_two == 'Q':
                card_two = 12
            elif card_two == 'K':
                card_two = 13
            elif card_two == 'A':
                card_two = 14
            else:
                card_one = int(card_one)

            if card_one <= card_two:
                return "DISCARD:" + game_data.current_hand[0]
            else:
                return "DISCARD:" + game_data.current_hand[1]'''
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

    if game_data.current_hand_strength > 0.55:
        # Decided this value after playing around with 0.50, 0.53, 0.55, 0.57,
        # 0.60, 0.70. %age of times we'd play given these thresholds: 0.50(40.72%), 0.53(32.12%), 0.55(25.18%),
        # 0.57(19.31%), 0.60(11.31%), 0.70(2.71%)
        game_data.aggression_factor = True

    if game_data.aggression_factor:
        limits = game_data.legal_action('BET')
        if limits is not None:
            if game_data.current_pot_size <= game_data.big_blind * 2:
                bet = (limits[0] + limits[1]) / 2
                if bet < limits[0]:
                    bet = limits[0]
                return 'BET:' + str(bet)
            else:
                bet = min(game_data.current_pot_size * 5 / 3, (limits[0] + limits[1]) / 2)
                if bet < limits[0]:
                    bet = limits[0]
                return 'BET:' + str(bet)
        else:
            limits = game_data.legal_action('RAISE')
            if limits is not None:
                if game_data.button and not game_data.has_four_bet:
                    bet = min(game_data.current_pot_size * 5 / 3, (limits[0] + limits[1]) / 2)
                    if bet < limits[0]:
                        bet = limits[0]
                    return 'RAISE:' + str(bet)
                elif not game_data.button and not game_data.has_three_bet:
                    bet = min(game_data.current_pot_size * 5 / 3, (limits[0] + limits[1]) / 2)
                    if bet < limits[0]:
                        bet = limits[0]
                    return 'RAISE:' + str(bet)
                elif game_data.current_hand_strength >= 0.573 and not game_data.has_bet_aggressively:
                    bet = min(game_data.current_pot_size * 5 / 3, (limits[0] + limits[1]) / 2)
                    game_data.has_bet_aggressively = True
                    if bet < limits[0]:
                        bet = limits[0]
                    return 'RAISE:' + str(bet)
                # PFR to be implemented here. When Aggressive, we want to RAISE 70% of the time and CALL 30% of the
                    # time.
        limits = game_data.legal_action('CALL')
        if limits:
            return 'CALL'
        else:
            return 'CHECK'
    else:
        limits = game_data.legal_action('CHECK')
        if limits:
            return 'CHECK'
        else:
            return 'FOLD'
# Change bet sizes to max of 2/3rd of Pot Size and odds*(average of min and max)
# Discard Strategy Gen[1]:
# WHEN to discard
# WHAT to discard
# How to interface with discards in the engine
