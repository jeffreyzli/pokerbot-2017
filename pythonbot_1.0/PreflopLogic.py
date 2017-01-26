
def action(game_data):

    # if button is True, you are dealer --> you act first pre-flop, then act second

    # pre-flop

    aggressive = False
    if game_data.aggression_factor or game_data.current_hand_strength > 0.55:  # Decided this value after playing around with 0.50, 0.53, 0.55, 0.57,
        # 0.60, 0.70. %age of times we'd play given these thresholds: 0.50(40.72%), 0.53(32.12%), 0.55(25.18%),
        # 0.57(19.31%), 0.60(11.31%), 0.70(2.71%)
        aggressive = True
        game_data.aggression_factor = True

    if aggressive:  # Want to set VPIP to low-end of 23-32%. (0.55 threshold ==> play 25.18% of time).

        # MAKE BOT STOP BETTING AFTER 3-BET (SOMEHOW COUNT OUR BETS). Set to bet/raise 4xBB
        limits = game_data.legal_action('RAISE')
        if limits is not None:
            if game_data.button:
                if not game_data.has_two_bet:  # Ideally, should prevent more than 3-bet
                    bet = min(game_data.big_blind * 4 + limits[0], limits[1])
                    if bet < limits[0]:
                        bet = limits[0]
                    return "RAISE:" + str(bet)
                elif game_data.current_hand_strength >= 0.573 and not game_data.has_bet_aggressively:  # PFR to be
                    # implemented here. When Aggressive, we want to RAISE 70% of the time and CALL 30% of the time.
                    bet = min(game_data.big_blind * 4 + limits[0], limits[1])
                    # threshold of 0.575(17.19%), 0.571(18.04%) || Want a threshold that plays 17.626% of time here.
                    game_data.has_bet_aggressively = True
                    if bet < limits[0]:
                        bet = limits[0]
                    return "RAISE:" + str(bet)
            else:
                if not game_data.has_three_bet:
                    bet = min(game_data.big_blind * 4 + limits[0], limits[1])
                    if bet < limits[0]:
                        bet = limits[0]
                    return "RAISE:" + str(bet)
                elif game_data.current_hand_strength >= 0.573 and not game_data.has_bet_aggressively:
                    # PFR to be implemented here. When Aggressive,
                    # we want to RAISE 70% of the time and CALL 30% of the time.
                    bet = min(game_data.big_blind * 4 + limits[0], limits[1])
                    # threshold of 0.575(17.19%), 0.571(18.04%) || Want a threshold that plays 17.626% of time here.
                    game_data.has_bet_aggressively = True
                    if bet < limits[0]:
                        bet = limits[0]
                    return "RAISE:" + str(bet)
                    # Keep raising 70% of the time. TO-DO: Decide when to stop Raising, and how much to Raise.
        return "CALL"
    else:
        if game_data.button and game_data.street_dict['0'] == 1:
            return "CALL"
        else:
            '''for move in moves:
            if "CALL" in move:          #TODO Return CALL iff lastAction by Player1 is NOT a RAISE of larger than a certain threshold. Else FOLD
                return "CALL"'''
            limit = game_data.legal_action("CHECK")
            if limit:
                return "CHECK"
            else:
                return "FOLD"

# EDITS: Separated PreflopLogic, Calculated %age of cards from each Threshold, Implemented VPIP and PFR stats [
# thepokerbank.com] Changed initial bet size to be proportional to strength of hand and be based on BB (4xBB) Decided
# when to stop raising and how much to raise subsequently. (Currently willing to 4-Bet.) TO-DO: Vary bets with
# slight randomness TO-DO: If they start calling huge and we aren't confident, FOLD.
