from deuces.deuces import Card, Evaluator


def discard_logic_post_flop(my_hand, board_cards):
    deck = ['2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d',
            '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Tc', 'Td', 'Th', 'Ts',
            'Jc', 'Jd', 'Jh', 'Js', 'Qc', 'Qd', 'Qh', 'Qs', 'Kc', 'Kd', 'Kh', 'Ks', 'Ac', 'Ad', 'Ah', 'As']

    # Deck = 52

    board = []
    for board_card in board_cards:
        board.append(Card.new(board_card))
        deck.remove(board_card)

    # Deck = 49

    hand = []
    for hand_card in my_hand:
        hand.append(Card.new(hand_card))
        deck.remove(hand_card)

    # Deck = 47

    evaluator = Evaluator()

    rank_no_discard = 0
    rank_h1_discard = 0
    rank_h0_discard = 0

    # rank_no_discard
    for card_one in deck:
        new_deck = list(deck)
        new_deck.remove(card_one)
        for card_two in new_deck:
            new_board = list(board)
            new_board += [Card.new(card_one), Card.new(card_two)]
            rank_no_discard += evaluator.evaluate(hand, new_board)
    rank_no_discard /= (47 * 46)

    # rank_h1_discard:
    for card_one in deck:
        new_hand = [Card.new(my_hand[0]), Card.new(card_one)]  # Discard my_hand[1]
        new_deck = list(deck)
        new_deck.remove(card_one)
        for card_two in new_deck:
            new_board = list(board)
            new_board += [Card.new(card_two)]
            rank_h1_discard += evaluator.evaluate(new_hand, new_board)
    rank_h1_discard /= (47 * 46)

    # rank_h0_discard:
    for card_one in deck:
        new_hand = [Card.new(card_one), Card.new(my_hand[1])]  # Discard myHand[0]
        new_deck = list(deck)
        new_deck.remove(card_one)
        for card_two in new_deck:
            new_board = list(board)
            new_board += [Card.new(card_two)]
            rank_h0_discard += evaluator.evaluate(new_hand, new_board)
    rank_h0_discard /= (47 * 46)

    best_rank = min(rank_no_discard, rank_h1_discard, rank_h0_discard)

    if best_rank is rank_no_discard:
        return False, None
    elif best_rank is rank_h1_discard:
        return True, my_hand[1]
    else:
        return True, my_hand[0]

        # return (True, discard) OR return (False, None)


def discard_logic_post_turn(my_hand, board_cards, discarded_card=None):
    deck = ['2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d',
            '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Tc', 'Td', 'Th', 'Ts',
            'Jc', 'Jd', 'Jh', 'Js', 'Qc', 'Qd', 'Qh', 'Qs', 'Kc', 'Kd', 'Kh', 'Ks', 'Ac', 'Ad', 'Ah', 'As']

    # Deck = 52

    board = []
    for board_card in board_cards:
        board.append(Card.new(board_card))
        deck.remove(board_card)

    # Deck = 48

    hand = []
    for hand_card in my_hand:
        hand.append(Card.new(hand_card))
        deck.remove(hand_card)

    # Deck = 46
    adjust = 0

    if discarded_card is not None:
        deck.remove(discarded_card)
        adjust += 1

    # Deck = 46 or 45

    evaluator = Evaluator()

    rank_no_discard = 0
    rank_h1_discard = 0
    rank_h0_discard = 0

    # rank_no_discard
    for card_one in deck:
        new_board = list(board)
        new_board += [Card.new(card_one)]
        rank_no_discard += evaluator.evaluate(hand, new_board)
    rank_no_discard /= (46 - adjust)

    # rank_h1_discard:
    for card_one in deck:
        new_hand = [Card.new(my_hand[0]), Card.new(card_one)]  # Discard myHand[1]
        new_deck = list(deck)
        new_deck.remove(card_one)
        for card_two in new_deck:
            new_board = list(board)
            new_board += [Card.new(card_two)]
            rank_h1_discard += evaluator.evaluate(new_hand, new_board)
    rank_h1_discard /= ((46 - adjust) * (45 - adjust))

    # rank_h0_discard:
    for card_one in deck:
        new_hand = [Card.new(card_one), Card.new(my_hand[1])]  # Discard myHand[0]
        new_deck = list(deck)
        new_deck.remove(card_one)
        for card_two in new_deck:
            new_board = list(board)
            new_board += [Card.new(card_two)]
            rank_h0_discard += evaluator.evaluate(new_hand, new_board)
    rank_h0_discard /= ((46 - adjust) * (45 - adjust))

    best_rank = min(rank_no_discard, rank_h1_discard, rank_h0_discard)

    if best_rank is rank_no_discard:
        return False, None
    elif best_rank is rank_h1_discard:
        return True, my_hand[1]
    else:
        return True, my_hand[0]

        # return (True, discard) OR return (False, None)
