import argparse
import socket
import sys

from GameData import GameData

import BetFoldLogic as BetFold


class Player:

    def run(self, input_socket):
        f_in = input_socket.makefile()

        while True:
            data = f_in.readline().strip()
            if not data:
                print "Gameover, engine disconnected."
                break

            data_list = data.split()
            word = data_list[0]

            if word == "NEWGAME":
                game_data = GameData(data_list[1], data_list[2], data_list[3], data_list[4])

            elif word == "NEWHAND":
                game_data.new_hand(data_list)

            elif word == "GETACTION":
                game_data.get_action(data_list)
                action = BetFold.action(game_data)
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
