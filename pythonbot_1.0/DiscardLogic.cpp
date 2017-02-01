//
//  DiscardLogic.cpp
//  NewBot
//
//  Created by Christien Williams on 1/31/17.
//
//

// vector::push_back
#include <iostream>
#include <vector>


#include "DiscardLogic.hpp"


int rank_h0_discard = 0
int count = 0


// rank_no_discard

for(std:vector<int>::iterator card_one = deck.begin(); card_one != deck.end(); ++card_one){
    std::vector<int>::iterator check1;
    std::vector<int>::iterator check2;
    check1 = find (board_cards.begin(), board_cards.end(), card_one);
    check2 = find (my_hand.begin(), my_hand.end(), card_one);
    if (check1 == myvector.end()) && (check2 == myvector.end()){
        for(std::vector<int>::iterator card_two = deck.begin(); card_two != deck.end(); ++card_two{
            std::vector<int>::iterator check21;
            std::vector<int>::iterator check22;
            check21 = find (board_cards.begin(), board_cards.end(), card_one);
            check22 = find (my_hand.begin(), my_hand.end(), card_one);
            if (check1 == myvector.end()) && (check2 == myvector.end())&& (card_two != card_one){
                ++count;
            }
        }
    }
}
            
            



// rank_h1_discard

int count = 0

for(std::vector<int>::iterator card_one = deck.begin(); card_one != deck.end(); ++card_one) {
    std::vector<int>::iterator check1;
    std::vector<int>::iterator check2;
    check1 = find (board_cards.begin(), board_cards.end(), card_one);
    check2 = find (my_hand.begin(), my_hand.end(), card_one);
    if (check1 == myvector.end()) && (check2 == myvector.end()){
        for (std::vector<int>::iterator card_two = deck.begin(); card_two != deck.end(); ++card_two){
            std::vector<int>::iterator check1;
            std::vector<int>::iterator check2;
            check1 = find (board_cards.begin(), board_cards.end(), card_one);
            check2 = find (my_hand.begin(), my_hand.end(), card_one);
            if (check1 == myvector.end()) && (check2 == myvector.end()) && (card_two != card_one){
                for (std::vector<int>::iterator card_three = deck.begin(); card_three != deck.end(); ++card_three){
                    std::vector<int>::iterator check1;
                    std::vector<int>::iterator check2;
                    check1 = find (board_cards.begin(), board_cards.end(), card_one);
                    check2 = find (my_hand.begin(), my_hand.end(), card_one);
                    if (check1 == myvector.end()) && (check2 == myvector.end()) && (card_two == card_three){
                            ++count;
                    }
                }
            }
        }
    }
}
    
// rank_h0_discard
        
int count = 0
            
for(std::vector<int>::iterator card_one = deck.begin(); card_one != deck.end(); ++card_one) {
    std::vector<int>::iterator check1;
    std::vector<int>::iterator check2;
    check1 = find (board_cards.begin(), board_cards.end(), card_one);
    check2 = find (my_hand.begin(), my_hand.end(), card_one);
    if (check1 == myvector.end()) && (check2 == myvector.end()){
        for (std::vector<int>::iterator card_two = deck.begin(); card_two != deck.end(); ++card_two){
            std::vector<int>::iterator check1;
            std::vector<int>::iterator check2;
            check1 = find (board_cards.begin(), board_cards.end(), card_one);
            check2 = find (my_hand.begin(), my_hand.end(), card_one);
            if (check1 == myvector.end()) && (check2 == myvector.end()) && (card_two != card_one){
                for (std::vector<int>::iterator card_three = deck.begin(); card_three != deck.end(); ++card_three){
                    std::vector<int>::iterator check1;
                    std::vector<int>::iterator check2;
                    check1 = find (board_cards.begin(), board_cards.end(), card_one);
                    check2 = find (my_hand.begin(), my_hand.end(), card_one);
                    if (check1 == myvector.end()) && (check2 == myvector.end()) && (card_two == card_three){
                        ++count;
                    }
                }
            }
        }
    }
}
