from HandRankings import hand_win_odds


def getaction(streetDict, potsize, numBoardCards, boardCards, numLastActions, lastActions, numMoves, moves, myHand, button):

    #if button is True, you are dealer --> you act first pre-flop, then act second

    #pre-flop

    odds = hand_win_odds(myHand)
    aggressive = False
    if odds > 0.55:     #Decided this value after playing around with 0.50, 0.53, 0.55, 0.57, 0.60, 0.70
                        #%age of times we'd play given these thresholds: 0.50(40.72%), 0.53(32.12%), 0.55(25.18%), 0.57(19.31%), 0.60(11.31%), 0.70(2.71%)
        aggressive = True
    betBool = False     #is Bet a legal move?
    raiseBool = False   #is Raise a legal move?

    if aggressive: #want to set VPIP to low-end of 23-32%. (0.55 threshold ==> play 25.18% of time).
        for move in moves:
            if "BET" in move:
                betBool = True
                raiseBool = False

                colIndex = move.index(":")  # Parses the min and max bet
                firstSlice = move[colIndex + 1:]
                colIndex2 = firstSlice.index(":")
                minBet = int(firstSlice[:colIndex2]) #int(move[colIndex + 1:colIndex2])
                maxBet = int(firstSlice[colIndex2 + 1:]) #int(move[colIndex2 + 1:])
            elif "RAISE" in move:
                betBool = False
                raiseBool = True

                colIndex = move.index(":")  # Parses the min and max bet
                firstSlice = move[colIndex + 1:]
                colIndex2 = firstSlice.index(":")
                minRaise = int(firstSlice[:colIndex2]) #int(move[colIndex + 1:colIndex2])
                maxRaise = int(firstSlice[colIndex2 + 1:]) #int(move[colIndex2 + 1:])

#MAKE BOT STOP BETTING AFTER 3-BET (SOMEHOW COUNT OUR BETS)
        if betBool and streetDict['0'] < 2:                                         #Ideally, should prevent more than 3-bet
            betSize = min(8 + minBet, maxBet)
            return "BET:" + str(betSize)                                    #Set to bet/raise 4xBB
        elif raiseBool and streetDict['0'] < 2:                                     #TIdeally, should prevent more than 3-bet
            betSize = min(8 + minRaise, maxRaise)
            return "RAISE:" + str(betSize)
        elif odds >= 0.573 and raiseBool and streetDict['0'] < 3:       #PFR to be implemented here. When Aggressive, we want to RAISE 70% of the time and CALL 30% of the time.
            print("SUPER AGGRESSIVE")
            betSize = min(8 + minRaise, maxRaise)                              #threshold of 0.575(17.19%), 0.571(18.04%) || Want a threshold that plays 17.626% of time here.
            return "RAISE:" + str(betSize)                    #Keep raising 70% of the time. TO-DO: Decide when to stop Raising, and how much to Raise.
        else:
            return "CALL"

    else:
        '''for move in moves:
            if "CALL" in move:          #TODO Return CALL iff lastAction by Player1 is NOT a RAISE of larger than a certain threshold. Else FOLD
                return "CALL"'''
        return "CHECK"

#EDITS
#Separated PreflopLogic, Calculated %age of cards from each Threshold, Implemented VPIP and PFR stats [thepokerbank.com]
#Changed initial bet size to be proportional to strength of hand and be based on BB (4xBB)
#Decided when to stop raising and how much to raise subsequently. (Currently willing to 4-Bet.)
    #TO-DO: Vary bets with slight randomness
    #TO-DO: If they start calling huge and we aren't confident, FOLD.