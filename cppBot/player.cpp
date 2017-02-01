#include <iostream>
#include "player.hpp"

Player::Player() {
}

void Player::run(tcp::iostream &stream) {
    std::string line;
    
    std::string new_game("NEWGAME");
    std::string new_hand("NEWHAND");
    std::string get_action("GETACTION");
    std::string hand_over("HANDOVER");
    std::string request_keyvalue_action("REQUESTKEYVALUES");
    std::string true_string("true");
    std::string first_word;
    std::string action;
    int index_one;
    int index_two;
    
    GameData game_data;
    
    while (std::getline(stream, line)) {
        std::cout << line << "\n";
        
        index_one = line.find_first_of(' ');
        first_word = line.substr(0, index_one));
        if (new_game.compare(first_word) == 0) {
            // extract information from packet
            index_one += 1;
            index_two = line.find(index_one, ' ');
            game_data.name = line.substr(index_one, index_two-index_one);
            index_two += 1;
            index_one = line.find(index_two, ' ');
            game_data.opponent_name = line.substr(index_two, index_one-index_two);
            index_one += 1;
            index_two = line.find(index_one, ' ');
            index_two += 1;
            index_one = line.find(index_two, ' ');
            game_data.big_blind = atoi(line.substr(index_two, index_one-index_two).c_str());
            index_one = line.find_last_of(' ');
            index_one += 1;
            game_data.time_bank = line.substr(index_one, line.length()-index_one);
        } else if (new_hand.compare(first_word) == 0) {
            // extract information from packet
            index_one += 1;
            index_two = line.find(index_one, ' ');
            game_data.hand_id = line.substr(index_one, index_two-index_one);
            index_two += 1;
            index_one = line.find(index_two, ' ');
            game_data.button = true_string.compare(line.substr(index_two, index_one-index_two)) == 0;
            index_one += 1;
            index_two = line.find(index_one, ' ');
            game_data.card_one = line.substr(index_one, index_two-index_one);
            index_two += 1;
            index_one = line.find(index_two, ' ');
            game_data.card_two = line.substr(index_two, index_one-index_two);
            index_one = line.find_last_of(' ');
            index_one += 1;
            game_data.time_bank = line.substr(index_one, line.length()-index_one);
        } else if (get_action.compare(first_word) == 0) {
            // extract information from packet
            index_one += 1;
            index_two = line.find(index_one, ' ');
            game_data.pot_size = atoi(line.substr(index_one, index_two-index_one).c_str());
            index_two += 1;
            index_one = line.find(index_two, ' ');
            int num_board_cards = atoi(line.substr(index_two, index_one-index_two).c_str());
            for (int i = 0; i < num_board_cards; i++) {
                if (i % 2 == 0) {
                    if(game_data.board_cards[i].compare("") == 0) {
                        index_one += 1;
                        index_two = line.find(index_one, ' ');
                        game_data.board_cards[i] = line.substr(index_one, index_two-index_one);
                    }
                } else {
                    if(game_data.board_cards[i].compare("") == 0) {
                        index_two += 1;
                        index_one = line.find(index_two, ' ');
                        game_data.board_cards[i] = line.substr(index_two, index_one-index_two);
                    }
                }
            }
            int num_last_actions;
            if (num_board_cards % 2 == 0) {
                index_one += 1;
                index_two = line.find(index_one, ' ');
                num_last_actions = atoi(line.substr(index_one, index_two-index_one).c_str());
            } else {
                index_two += 1;
                index_one = line.find(index_two, ' ');
                num_last_actions = atoi(line.substr(index_two, index_one-index_two).c_str());
            }
            std::str last_actions[num_last_actions];
            for (int i = 0; i < num_last_actions; i++) {
                if(num_board_cards % 2 != 0) {
                    if (i % 2 == 0) {
                        index_one += 1;
                        index_two = line.find(index_one, ' ');
                        last_actions[i] = line.substr(index_one, index_two-index_one);
	                } else {
                        index_two += 1;
                        index_one = line.find(index_two, ' ');
                        last_actions[i] = line.substr(index_two, index_one-index_two);
	                }
                } else {
                    if (i % 2 != 0) {
                        index_one += 1;
                        index_two = line.find(index_one, ' ');
                        last_actions[i] = line.substr(index_one, index_two-index_one);
                    } else {
                        index_two += 1;
                        index_one = line.find(index_two, ' ');
                        last_actions[i] = line.substr(index_two, index_one-index_two);
                    }
                }
            }
            int num_legal_actions;
            if (num_board_cards % 2 == 0 && num_last_actions % 2 != 0) {
                index_one += 1;
                index_two = line.find(index_one, ' ');
                num_legal_actions = atoi(line.substr(index_one, index_two-index_one).c_str());
            } else {
                index_two += 1;
                index_one = line.find(index_two, ' ');
                num_legal_actions = atoi(line.substr(index_two, index_one-index_two).c_str());
            }
            std::str legal_actions[num_legal_actions];
            for (int i = 0; i < num_legal_actions; i++) {
                if(num_board_cards % 2 != 0 && num_last_actions == 0) {
                    if (i % 2 == 0) {
                        index_one += 1;
                        index_two = line.find(index_one, ' ');
                        legal_actions[i] = line.substr(index_one, index_two-index_one);
                    } else {
                        index_two += 1;
                        index_one = line.find(index_two, ' ');
                        legal_actions[i] = line.substr(index_two, index_one-index_two);
                    }
                } else {
                    if (i % 2 != 0) {
                        index_one += 1;
                        index_two = line.find(index_one, ' ');
                        legal_actions[i] = line.substr(index_one, index_two-index_one);
                    } else {
                        index_two += 1;
                        index_one = line.find(index_two, ' ');
                        legal_actions[i] = line.substr(index_two, index_one-index_two);
                    }
                }
            }
            index_one = line.find_last_of(' ');
            index_one += 1;
            game_data.time_bank = line.substr(index_one, line.length()-index_one);
            std::cout << game_data.pot_size << " " << num_board_cards << " " << num_last_actions << " " << num_legal_actions << " " << game_data.time_bank;
            for (int i = 0; i < num_board_cards; i++) {
                std::cout << game_data.board_cards[i] << endl;
            }
            for (int i = 0; i < num_last_actions; i++) {
                std::cout << last_actions[i] << endl;
            }
            for (int i = 0; i < num_legal_actions; i++) {
                std::cout << legal_actions[i] << endl;
            }
            action = "CHECK";
        } else if (hand_over.compare(first_word) == 0) {
            index_one = line.find_last_of(' ');
            index_one += 1;
            game_data.time_bank = line.substr(index_one, line.length()-index_one);
        } else if (request_keyvalue_action.compare(first_word) == 0) {
            action = "FINISH";
        }
        
        stream << action << "\n";
    }

    std::cout << "Gameover, engine disconnected.\n";
}

struct GameData {
    std::string name;
    std::string opponent_name;
    std::string big_blind;
    std::string time_bank;
    int hand_id;
    bool button;
    int pot_size;
    std::string card_one;
    std::string card_two;
    std::string hand_strength;
    std::string board_cards[5];
};
