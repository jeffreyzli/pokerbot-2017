
def action(game_data):

    # post-river

    aggressive = False
    if game_data.current_hand_strength > 0.55:  # Decided this value after playing around with 0.50, 0.53, 0.55,
        # 0.57, 0.60, 0.70
        aggressive = True

    if aggressive:
        limit = game_data.legal_action('BET')
        if limit is not None:
            if game_data.current_pot_size <= game_data.big_blind * 2:
                bet = (limit[0] + limit[1]) / 2
                return 'BET:' + str(bet)
            else:
                bet = min(game_data.current_pot_size * 5 / 3, (limit[0] + limit[1]) / 2)
                return 'BET:' + str(bet)
        else:
            limit = game_data.legal_action('RAISE')
            if limit is not None:
                if game_data.button and not game_data.has_four_bet:
                    bet = min(game_data.current_pot_size * 5 / 3, (limit[0] + limit[1]) / 2)
                    return 'RAISE:' + str(bet)
                elif not game_data.button and not game_data.has_three_bet:
                    bet = min(game_data.current_pot_size * 5 / 3, (limit[0] + limit[1]) / 2)
                    return 'RAISE:' + str(bet)
                elif game_data.current_hand_strength >= 0.573 and not game_data.has_bet_aggressively:
                    bet = min(game_data.current_pot_size * 5 / 3, (limit[0] + limit[1]) / 2)
                    game_data.has_bet_aggressively = True
                    return 'RAISE:' + str(bet)
                # PFR to be implemented here. When Aggressive, we want to RAISE 70% of the time and CALL 30% of the
                    # time.
        return "CALL"
    else:
        return "CHECK"
# Change bet sizes to max of 2/3rd of Pot Size and odds*(average of min and max)
# Discard Strategy Gen[1]:
# WHEN to discard
# WHAT to discard
# How to interface with discards in the engine
