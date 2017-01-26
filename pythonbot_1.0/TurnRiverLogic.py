
def action(game_data):

    # post-turn, pre-river

    if game_data.discard:
        if game_data.current_hand_strength <= 0.55:  # WE ARE GOING TO DISCARD
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
                return "DISCARD:" + game_data.current_hand[0] + "\n"
            else:
                return "DISCARD:" + game_data.current_hand[1] + "\n"
        else:
            game_data.discard = False

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
