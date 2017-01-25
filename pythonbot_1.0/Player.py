import argparse
import socket
import sys
from HandRankings import hand_win_odds

import PreflopLogic as pl
import FlopTurnLogic as ft
import TurnRiverLogic as tr
import PostRiverLogic as pf

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player:


    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()

        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.

            data_list = data.split()
            word = data_list[0]

            if word == "NEWGAME":
                ourName = data_list[1]

            if word == "NEWHAND":
                hand = [data_list[3], data_list[4]]
                odds = hand_win_odds(hand)
                button = data_list[2]
                streetDict = {'0':0, '3':0, '4':0, '5':0} ##TODO - ADDED DICTIONARY FOR 3-BET LIMITING
                didDiscard = False



            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            if word == "GETACTION":
                action = None
                potsize = int(data_list[1])
                numBoardCards = int(data_list[2])
                boardCards = []  # list of cards on board; len 0, 3, 4, 5
                for i in range(numBoardCards):
                    boardCards.append(data_list[3 + i])

                index = 3 + numBoardCards
                numLastActions = int(data_list[index])
                lastActions = []  # list of previous actions in this hand
                for i in range(numLastActions):
                    lastActions.append(data_list[index + 1 + i])

                index2 = index + 1 + numLastActions
                numMoves = int(data_list[index2])
                moves = []  # list of legal moves
                for i in range(numMoves):
                    moves.append(data_list[index2 + 1 + i])

        #RaiseCounter Variable:
                if str(numBoardCards) in streetDict:
                    streetDict[str(numBoardCards)] += 1



                # At start of Flop, return DISCARD if current hand is not aggressive
                if (streetDict['3'] == 1 and streetDict['4'] == 0) or (streetDict['4'] == 1 and streetDict['5'] == 0):
                    if odds <= 0.55:  # WE ARE GOING TO DISCARD
    #TODO Need to decide WHICH card to discard. Currently discarding low card. Should later take into account boardCards.
                        didDiscard = True
                        cardsDict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                                     'J': 11, 'Q': 12, 'K': 13, 'A': 14}
                        val1 = cardsDict[hand[0][0]]
                        val2 = cardsDict[hand[1][0]]
                        if val1 <= val2:
                            action = ("DISCARD:" + hand[0] + "\n")
                        else:
                            action = ("DISCARD:" + hand[1] + "\n")

                # if didDiscard:          #Makes sure we only change our holeCards if WE were the one to just discard
                for pastAction in lastActions:
                    if "DISCARD" in pastAction and ourName in pastAction:
                        print("UGH MAMI")
                        Old_card_discard = pastAction[8:10]  # Parse old and new card result from Discard action
                        New_card = pastAction[11:13]
                        hand[hand.index(Old_card_discard)] = New_card  # Edit our holeCards list

                        # 1.) figure out current hand from holeCards[]
                        # 2.) parse DISCARD pastAction line (DISCARD:3h:6h:PLAYER) to extract variables Old_card_discard and New_card
                        # 3.) find new hand
                        # 4.) odds = hand_win_odds([Old_card_keep, New_card]) (THIS HAPPENS INSIDE THE LOGIC FILES)
                        break
                        # didDiscard = False

                # After discard, if current hand is now aggressive, turn aggressive to True.



                #decides what LOGIC to follow based on numBoardCards
                if action is None:
                    if numBoardCards == 0:
                        action = pl.getaction(streetDict, potsize, numBoardCards, boardCards, numLastActions, lastActions, numMoves, moves, hand, button)
                    elif numBoardCards == 3:
                        action = ft.getaction(streetDict, potsize, numBoardCards, boardCards, numLastActions, lastActions, numMoves, moves, hand, button)
                    elif numBoardCards == 4:
                        action = tr.getaction(streetDict, potsize, numBoardCards, boardCards, numLastActions, lastActions, numMoves, moves, hand, button)
                    else:
                        action = pf.getaction(streetDict, potsize, numBoardCards, boardCards, numLastActions, lastActions, numMoves, moves, hand, button)
                #print(str(hand) + ", " + str(odds))
                s.send(action + "\n")
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
