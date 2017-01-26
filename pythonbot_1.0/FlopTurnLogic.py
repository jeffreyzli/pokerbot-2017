from DiscardLogic import discard_logic_post_flop as discard_logic
#from DiscardLogic56 import discard_logic_post_flop as discard_logic
#from DiscardLogicSimple import discard_logic_post_flop as discard_logic


def action(game_data):

    # if button is True, you are dealer --> you act first pre-flop, then act second post-flop

    # post-flop, pre-turn

    if game_data.discard:
        discard, card = discard_logic(game_data.current_hand, game_data.board_cards)
        if discard:
            game_data.discarded_flop_card = card
            return 'DISCARD:' + card
        else:
            game_data.discard = False

    aggressive = False
    if game_data.aggression_factor or game_data.current_hand_strength > 0.55:  # Decided this value after playing around with 0.50, 0.53, 0.55, 0.57,
        # 0.60, 0.70. %age of times we'd play given these thresholds: 0.50(40.72%), 0.53(32.12%), 0.55(25.18%),
        # 0.57(19.31%), 0.60(11.31%), 0.70(2.71%)
        aggressive = True
        game_data.aggression_factor = True

    if aggressive:
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