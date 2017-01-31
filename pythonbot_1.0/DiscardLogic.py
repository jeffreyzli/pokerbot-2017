from deuces.deuces import Card, Evaluator


def discard_logic_post_flop(my_hand, board_cards, deck):

    # Deck = 52

    board = []
    for board_card in board_cards:
        board.append(Card.new(board_card))

    # Deck = 49

    hand = []
    for hand_card in my_hand:
        hand.append(Card.new(hand_card))

    # Deck = 47

    evaluator = Evaluator()

    rank_no_discard = 0
    rank_h1_discard = 0
    rank_h0_discard = 0

    # rank_no_discard
    count = 0
    for card_one in deck:
        if card_one not in my_hand and card_one not in board_cards:
            for card_two in deck:
                if card_two not in my_hand and card_two not in board_cards and card_two is not card_one:
                    new_board = list(board)
                    new_board += [Card.new(card_one), Card.new(card_two)]
                    count += 1
                    # rank_no_discard += evaluator.evaluate(hand, new_board)
    rank_no_discard /= (47 * 46)

    # rank_h1_discard:
    count = 0
    for card_one in deck:
        if card_one not in my_hand and card_one not in board_cards:
            new_hand = [Card.new(my_hand[0]), Card.new(card_one)]  # Discard my_hand[1]
            for card_two in deck:
                if card_two not in my_hand and card_two not in board_cards and card_two is not card_one:
                    for card_three in deck:
                        if card_three not in my_hand and card_three not in board_cards and card_three is not card_two:
                            new_board = list(board)
                            new_board += [Card.new(card_two), Card.new(card_three)]
                            count += 1
                            # rank_h1_discard += evaluator.evaluate(new_hand, new_board)
    rank_h1_discard /= (47 * 46 * 45)

    count = 0
    # rank_h0_discard:
    for card_one in deck:
        if card_one not in my_hand and card_one not in board_cards:
            new_hand = [Card.new(card_one), Card.new(my_hand[1])]  # Discard myHand[0]
            for card_two in deck:
                if card_two not in my_hand and card_two not in board_cards:
                    for card_three in deck:
                        if card_three not in my_hand and card_three not in board_cards and card_three is not card_two:
                            new_board = list(board)
                            new_board += [Card.new(card_two), Card.new(card_three)]
                            count += 1
                            # rank_h0_discard += evaluator.evaluate(new_hand, new_board)
    rank_h0_discard /= (47 * 46 * 45)

    best_rank = min(rank_no_discard, rank_h1_discard, rank_h0_discard)

    if best_rank is rank_no_discard:
        return False, None
    elif best_rank is rank_h1_discard:
        return True, my_hand[1]
    else:
        return True, my_hand[0]

        # return (True, discard) OR return (False, None)


def discard_logic_post_turn(my_hand, board_cards, deck, discarded_card=None):

    # Deck = 52

    board = []
    for board_card in board_cards:
        board.append(Card.new(board_card))

    # Deck = 48

    hand = []
    for hand_card in my_hand:
        hand.append(Card.new(hand_card))

    # Deck = 46
    adjust = 0

    if discarded_card is not None:
        adjust += 1

    # Deck = 46 or 45

    evaluator = Evaluator()

    rank_no_discard = 0
    rank_h1_discard = 0
    rank_h0_discard = 0

    # rank_no_discard
    for card_one in deck:
        if card_one not in my_hand and card_one not in board_cards:
            new_board = list(board)
            new_board += [Card.new(card_one)]
            rank_no_discard += evaluator.evaluate(hand, new_board)
    rank_no_discard /= (46 - adjust)

    # rank_h1_discard:
    count = 0
    for card_one in deck:
        if card_one not in my_hand and card_one not in board_cards:
            new_hand = [Card.new(my_hand[0]), Card.new(card_one)]  # Discard myHand[1]
            for card_two in deck:
                if card_two not in my_hand and card_two not in board_cards and card_two is not card_one:
                    new_board = list(board)
                    new_board += [Card.new(card_two)]
                    count += 1
                    # rank_h1_discard += evaluator.evaluate(new_hand, new_board)
    rank_h1_discard /= ((46 - adjust) * (45 - adjust))

    # rank_h0_discard:
    count = 0
    for card_one in deck:
        if card_one not in my_hand and card_one not in board_cards:
            new_hand = [Card.new(card_one), Card.new(my_hand[1])]  # Discard myHand[0]
            for card_two in deck:
                if card_two not in my_hand and card_two not in board_cards and card_two is not card_one:
                    new_board = list(board)
                    new_board += [Card.new(card_two)]
                    count += 1
                    # rank_h0_discard += evaluator.evaluate(new_hand, new_board)
    rank_h0_discard /= ((46 - adjust) * (45 - adjust))

    best_rank = min(rank_no_discard, rank_h1_discard, rank_h0_discard)

    if best_rank is rank_no_discard:
        return False, None
    elif best_rank is rank_h1_discard:
        return True, my_hand[1]
    else:
        return True, my_hand[0]

        # return (True, discard) OR return (False, None)
