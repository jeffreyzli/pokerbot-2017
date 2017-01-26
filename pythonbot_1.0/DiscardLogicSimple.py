#postTurn: IF 4 boardCards are the same suit AND IF both our cards are that suit --> discard lower one
#postTurn: IF 4 boardCards are the same suit AND IF only one of our cards are that suit --> discard the non-suited hand
#postTurn: IF 4 boardCards are the same suit AND IF we have no cards of that suit --> discard [LOW] card
#postTurn: IF 3 boardCards are the same suit AND IF both our cards are that suit --> no discard
#postTurn: IF 3 boardCards are the same suit AND IF only one of our cards are that suit --> discard the non-suited hand, IF no pairs anywhere

# if [A] [A] --> no discard
# elif [A] [B] with flop of [A] [C] [B] --> no discard
# elif [Low] [High] with flop of [Low] [B] [C] --> discard High
# else discard Low



def discard_logic_post_flop(my_hand, board_cards):
    cardsDict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    val1 = cardsDict[my_hand[0][0]]
    val2 = cardsDict[my_hand[1][0]]

    # if [A] [A] --> no discard
    if val1 == val2:
        return(False, None)
    # elif [A] [B] with flop of [A] [C] [B] --> no discard
    elif val1 in board_cards and val2 in board_cards:
        return(False, None)
    # elif [Low] [High] with flop of [Low] [B] [C] --> discard High
    elif min(val1, val2) in board_cards:
        if max(val1, val2) == val1:
            return(True, my_hand[0])
        else:
            return(True, my_hand[1])
    # else discard [Low]
    else:
        if min(val1, val2) == val1:
            return(True, my_hand[0])
        if min(val1, val2) == val2:
            return(True, my_hand[1])

    # return (True, discard) OR return (False, None)

def discard_logic_post_turn(my_hand, board_cards, discarded_card = None):
    cardsDict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suitDict = {'h': 0, 'd': 0, 's': 0, 'c': 0}

    val1 = cardsDict[my_hand[0][0]]
    val2 = cardsDict[my_hand[1][0]]
    suit = None
    hand_count = 0

    for board_card in board_cards:
        suitDict[board_card[1]] += 1

    # postTurn: IF 4 boardCards are the same suit AND
    if 4 in suitDict.values():
        for pair in suitDict.items():
            if pair[1] == 4:
                suit = pair[0]
                break
        for card in my_hand:
            if card[1] == suit:
                hand_count += 1

        # IF only one of our cards are that suit --> discard the non-suited hand
        if hand_count == 1:
            for card in my_hand:
                if card[1] is not suit:
                    return (True, card)

        # ELSE we have no cards of that suit OR we have both cards of that suit --> discard [LOW] card
        else:
            if min(val1, val2) == val1:
                return (True, my_hand[0])
            if min(val1, val2) == val2:
                return (True, my_hand[1])



    # postTurn: IF 3 boardCards are the same suit AND
    elif 3 in suitDict.values():
        for pair in suitDict.items():
            if pair[1] == 3:
                suit = pair[0]
                break
        for card in my_hand:
            if card[1] == suit:
                hand_count += 1

        # IF both our cards are that suit --> no discard
        if hand_count == 2:
            return (False, None)

        # IF only one of our cards are that suit --> discard the non-suited hand, IF no pairs anywhere
        elif hand_count == 1:
            if (val1 == val2) or (val1 in board_cards) or (val2 in board_cards):
                return (False, None)
            else:
                for card in my_hand:
                    if card[1] is not suit:
                        return (True, card)

        # IF no cards are that suit --> continue
        else:
            pass



    # if [A] [A] --> no discard
    elif val1 == val2:
        return(False, None)
    # elif [A] [B] with flop of [A] [C] [B] --> no discard
    elif val1 in board_cards and val2 in board_cards:
        return(False, None)
    # elif [Low] [High] with flop of [Low] [B] [C] --> discard High
    elif min(val1, val2) in board_cards:
        if max(val1, val2) == val1:
            return(True, my_hand[0])
        else:
            return(True, my_hand[1])
    # else discard [Low]
    else:
        if min(val1, val2) == val1:
            return(True, my_hand[0])
        if min(val1, val2) == val2:
            return(True, my_hand[1])

    # return (True, discard) OR return (False, None)