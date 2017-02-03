# post turn: IF 4 boardCards are the same suit AND IF both our cards are that suit --> discard lower one
# post turn: IF 4 boardCards are the same suit AND
# IF only one of our cards are that suit --> discard the non-suited hand
# post turn: IF 4 boardCards are the same suit AND IF we have no cards of that suit --> discard [LOW] card
# post turn: IF 3 boardCards are the same suit AND IF both our cards are that suit --> no discard
# post turn: IF 3 boardCards are the same suit AND
# IF only one of our cards are that suit --> discard the non-suited hand, IF no pairs anywhere

# if [A] [A] --> no discard
# elif [A] [B] with flop of [A] [C] [B] --> no discard
# elif [Low] [High] with flop of [Low] [B] [C] --> discard High
# else discard Low


def discard_logic_post_flop(my_hand, board_cards):
    cards_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                  'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suit_dict = {'h': 0, 'd': 0, 's': 0, 'c': 0}

    val_one = cards_dict[my_hand[0][0]]
    val_two = cards_dict[my_hand[1][0]]

    board_card_values = []
    for board_card in board_cards:
        suit_dict[board_card[1]] += 1
        board_card_values.append(cards_dict[board_card[0]])

# if low [A] [A] and [A] on table
    if val_one == val_two and val_one <= 6:
        if val_one in board_card_values:
            return False, None

    # if high [A] [A] --> no discard
    if val_one == val_two and val_one > 6:
        return False, None
# elif low [A] [A] --> discard first card, or if three table cards are same suit and if one card matches them, discard
    elif val_one == val_two and val_one <= 6:
        if suit_dict[my_hand[0][1]] == 3:
            return True, my_hand[1]
        else:
            return True, my_hand[0]
    # elif [A] [B] with flop of [A] [C] [B] --> no discard
    elif val_one in board_card_values and val_two in board_card_values:
        return False, None
# if low [A] [B] and [A] [A] on table --> no discard
    elif min(val_one, val_two) in board_card_values:
        new_board_card_values = []
        for board_card_value in board_card_values:
            new_board_card_values.append(board_card_value)
        new_board_card_values.remove(min(val_one, val_two))
        if min(val_one, val_two) in new_board_card_values:
            if max(val_one, val_two) == val_one:
                return True, my_hand[0]
            else:
                return True, my_hand[1]
    # elif [Low] [High] with flop of [Low] [B] [C] IF [Low] > 6 --> discard High
    if min(val_one, val_two) in board_card_values:
        if min(val_one, val_two) <= 6:
            if max(val_one, val_two) == val_one:
                return True, my_hand[1]
            else:
                return True, my_hand[0]
        elif max(val_one, val_two) == val_one:
            return True, my_hand[0]
        else:
            return True, my_hand[1]
    # else discard [Low]
    else:
        if min(val_one, val_two) == val_one:
            return True, my_hand[0]
        if min(val_one, val_two) == val_two:
            return True, my_hand[1]

            # return (True, discard) OR return (False, None)


def discard_logic_post_turn(my_hand, board_cards, discarded_card=None):
    if discarded_card is None:
        pass
    cards_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                  'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suit_dict = {'h': 0, 'd': 0, 's': 0, 'c': 0}

    val_one = cards_dict[my_hand[0][0]]
    val_two = cards_dict[my_hand[1][0]]
    suit = None
    hand_count = 0

    board_card_values = []
    for board_card in board_cards:
        suit_dict[board_card[1]] += 1
        board_card_values.append(cards_dict[board_card[0]])

    # postTurn: IF 4 boardCards are the same suit AND
    if 4 in suit_dict.values():
        for pair in suit_dict.items():
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
                    return True, card

        # ELSE we have no cards of that suit OR we have both cards of that suit --> discard [LOW] card
        else:
            if min(val_one, val_two) == val_one:
                return True, my_hand[0]
            if min(val_one, val_two) == val_two:
                return True, my_hand[1]

    # postTurn: IF 3 boardCards are the same suit AND
    elif 3 in suit_dict.values():
        for pair in suit_dict.items():
            if pair[1] == 3:
                suit = pair[0]
                break
        for card in my_hand:
            if card[1] == suit:
                hand_count += 1

        # IF both our cards are that suit --> no discard
        if hand_count == 2:
            return False, None

        # IF only one of our cards are that suit --> discard the non-suited card, IF no pairs anywhere
        elif hand_count == 1:
            if val_one == val_two or val_one in board_card_values or val_two in board_card_values:
                return False, None
            else:
                for card in my_hand:
                    if card[1] is not suit:
                        return True, card

        # IF no cards are that suit --> continue
    return discard_logic_post_flop(my_hand, board_cards)
    # return (True, discard) OR return (False, None)
