from HandRankings import hand_win_odds

def getaction(data_list, myHand, button):
    numBoardCards = int(data_list[2])
    boardCards = [] #list of cards on board; len 0, 3, 4, 5
    for i in range(numBoardCards):
        boardCards.append(data_list[3 + i])

    index = 3 + numBoardCards
    numLastActions = int(data_list[index])
    lastActions = [] #list of previous actions in this hand
    for i in range(numLastActions):
        lastActions.append(data_list[index + 1 + i])

    index2 = index + 1 + numLastActions
    numMoves = int(data_list[index2])
    moves = [] #list of legal moves
    for i in range(numMoves):
        moves.append(data_list[index2 + 1 + i])

    #if button is True, you are dealer --> you act first pre-flop, then act second

    #pre-flop
    odds = hand_win_odds(myHand)
    aggressive = False
    if odds > 0.55:     #Decided this value after playing around with 0.50, 0.53, 0.55, 0.57, 0.60, 0.70
        aggressive = True
    betBool = False     #is Bet a legal move?
    raiseBool = False   #is Raise a legal move?
    hasBetRaise = False #have I already bet or raised?

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
        if betBool and not hasBetRaise:
            return "BET:" + str(odds*(minBet + maxBet)/2) #arbitrarily set to bet odds * average of min/max bets
        elif raiseBool and not hasBetRaise:
            return "RAISE:" + str(odds * (minRaise + maxRaise) / 2)  # arbitrarily set to raise odds * average of min/max bets
        else:
            return "CALL"
    else:
        for move in moves:
            if "CALL" in move:
                return "CALL"
        return "CHECK"