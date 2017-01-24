from HandRankings import hand_win_odds


def getaction(streetDict, potsize, numBoardCards, boardCards, numLastActions, lastActions, numMoves, moves, myHand, button):

    # if button is True, you are dealer --> you act first pre-flop, then act second post-flop

    #postFlop, preTurn

    odds = hand_win_odds(myHand)
    aggressive = False
    if odds > 0.55:     #Decided this value after playing around with 0.50, 0.53, 0.55, 0.57, 0.60, 0.70
        aggressive = True
    betBool = False     #is Bet a legal move?
    raiseBool = False   #is Raise a legal move?

    if aggressive:
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
##TODO - SAME SHIT. MAKE THESE HAVE A BET LIMIT (MAYBE OF 1 INSTEAD OF 3)

        if betBool and streetDict['3'] < 2:                                         #TODO - Ideally, should prevent more than 3-bet
            betSize = min(potsize * 0.67, (minBet + maxBet) / 2)
            return "BET:" + str(betSize)
        elif raiseBool and streetDict['3'] < 2:                                     #TODO - Ideally, should prevent more than 3-bet
            betSize = min(potsize * 0.67, (minRaise + maxRaise) / 2)
            return "RAISE:" + str(betSize)
        elif odds >= 0.573 and raiseBool and streetDict['3'] < 3:       #PFR to be implemented here. When Aggressive, we want to RAISE 70% of the time and CALL 30% of the time.
            print("SUPER AGGRESSIVE")
            betSize = min(potsize * 0.67, (minRaise + maxRaise) / 2)
            return "RAISE:" + str(betSize)
        else:
            return "CALL"

    else:
        '''for move in moves:
            if "CALL" in move:
                return "CALL"'''
        return "CHECK"

#Change bet sizes to max of 2/3rd of Pot Size and odds*(average of min and max)

    #Discard Strategy Gen[1]:
        #WHEN to discard
        #WHAT to discard
    #How to interface with discards in the engine