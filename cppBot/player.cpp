#include <iostream>
#include "player.hpp"

Player::Player() {
}

void Player::run(tcp::iostream &stream) {
    std::string line;
    
    // deck
    std::string card_values[] = {"JOKER", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
    std::string card_suits[] = {"s", "d", "c", "h"};
    
    // pocket strengths
    std::map<std::string, double> pocket_strengths;
    pocket_strengths.insert(std::pair<std::string, double>("57s", 0.4103365704403352));
    pocket_strengths.insert(std::pair<std::string, double>("5Ks", 0.5367018102247861));
    pocket_strengths.insert(std::pair<std::string, double>("68o", 0.4070527662014068));
    pocket_strengths.insert(std::pair<std::string, double>("9As", 0.6172307285730803));
    pocket_strengths.insert(std::pair<std::string, double>("4Jo", 0.43949540398045656));
    pocket_strengths.insert(std::pair<std::string, double>("69o", 0.4213731085744624));
    pocket_strengths.insert(std::pair<std::string, double>("6Ko", 0.5233222275107092));
    pocket_strengths.insert(std::pair<std::string, double>("4Js", 0.4664950593705887));
    pocket_strengths.insert(std::pair<std::string, double>("TAs", 0.6341252986461375));
    pocket_strengths.insert(std::pair<std::string, double>("TAo", 0.6156803097345133));
    pocket_strengths.insert(std::pair<std::string, double>("6To", 0.4367067652576978));
    pocket_strengths.insert(std::pair<std::string, double>("QAs", 0.6522860804580483));
    pocket_strengths.insert(std::pair<std::string, double>("35o", 0.33234734723665876));
    pocket_strengths.insert(std::pair<std::string, double>("49o", 0.3815347005597221));
    pocket_strengths.insert(std::pair<std::string, double>("23s", 0.3286236094969284));
    pocket_strengths.insert(std::pair<std::string, double>("7Ao", 0.5715322241176861));
    pocket_strengths.insert(std::pair<std::string, double>("79o", 0.44239114211640623));
    pocket_strengths.insert(std::pair<std::string, double>("46s", 0.38724529944581176));
    pocket_strengths.insert(std::pair<std::string, double>("5Qo", 0.48284858547025045));
    pocket_strengths.insert(std::pair<std::string, double>("25s", 0.3457991718768043));
    pocket_strengths.insert(std::pair<std::string, double>("JAo", 0.6248118020129602));
    pocket_strengths.insert(std::pair<std::string, double>("46o", 0.35078378527033716));
    pocket_strengths.insert(std::pair<std::string, double>("6Jo", 0.45666249764800937));
    pocket_strengths.insert(std::pair<std::string, double>("3As", 0.563251325626585));
    pocket_strengths.insert(std::pair<std::string, double>("7Ko", 0.5346225723405311));
    pocket_strengths.insert(std::pair<std::string, double>("29o", 0.36796845621253343));
    pocket_strengths.insert(std::pair<std::string, double>("25o", 0.3118254095063885));
    pocket_strengths.insert(std::pair<std::string, double>("27o", 0.3178792188459772));
    pocket_strengths.insert(std::pair<std::string, double>("5Jo", 0.44925691196413253));
    pocket_strengths.insert(std::pair<std::string, double>("6Qs", 0.5163400857999437));
    pocket_strengths.insert(std::pair<std::string, double>("4Ks", 0.5309583125726623));
    pocket_strengths.insert(std::pair<std::string, double>("9Ks", 0.5867892508196991));
    pocket_strengths.insert(std::pair<std::string, double>("4Ts", 0.439786346626222));
    pocket_strengths.insert(std::pair<std::string, double>("9Ao", 0.5945813134269023));
    pocket_strengths.insert(std::pair<std::string, double>("39s", 0.4083654741321984));
    pocket_strengths.insert(std::pair<std::string, double>("QKs", 0.625163371660187));
    pocket_strengths.insert(std::pair<std::string, double>("36o", 0.33161356037288814));
    pocket_strengths.insert(std::pair<std::string, double>("JAs", 0.6436259307782882));
    pocket_strengths.insert(std::pair<std::string, double>("38o", 0.346955713432043));
    pocket_strengths.insert(std::pair<std::string, double>("47o", 0.3580520658232328));
    pocket_strengths.insert(std::pair<std::string, double>("24o", 0.2998933995648065));
    pocket_strengths.insert(std::pair<std::string, double>("JQo", 0.5707444131683874));
    pocket_strengths.insert(std::pair<std::string, double>("QQo", 0.796980237504431));
    pocket_strengths.insert(std::pair<std::string, double>("89o", 0.46024466527660707));
    pocket_strengths.insert(std::pair<std::string, double>("56o", 0.371915724019316));
    pocket_strengths.insert(std::pair<std::string, double>("7As", 0.5966644031865384));
    pocket_strengths.insert(std::pair<std::string, double>("9Qs", 0.5626572391679684));
    pocket_strengths.insert(std::pair<std::string, double>("58o", 0.388504544202699));
    pocket_strengths.insert(std::pair<std::string, double>("5Ao", 0.5583593775883204));
    pocket_strengths.insert(std::pair<std::string, double>("67s", 0.42947430791006946));
    pocket_strengths.insert(std::pair<std::string, double>("3To", 0.39912244299476013));
    pocket_strengths.insert(std::pair<std::string, double>("26o", 0.3116596638655462));
    pocket_strengths.insert(std::pair<std::string, double>("3Qs", 0.48788224215691134));
    pocket_strengths.insert(std::pair<std::string, double>("27s", 0.35395290712970273));
    pocket_strengths.insert(std::pair<std::string, double>("29s", 0.4009237261384592));
    pocket_strengths.insert(std::pair<std::string, double>("49s", 0.41347378168769533));
    pocket_strengths.insert(std::pair<std::string, double>("TKs", 0.6031672178002293));
    pocket_strengths.insert(std::pair<std::string, double>("24s", 0.33949473192072));
    pocket_strengths.insert(std::pair<std::string, double>("7Jo", 0.4764203100466618));
    pocket_strengths.insert(std::pair<std::string, double>("8Ts", 0.5078444407512049));
    pocket_strengths.insert(std::pair<std::string, double>("KKo", 0.818983453878926));
    pocket_strengths.insert(std::pair<std::string, double>("26s", 0.3470384659965889));
    pocket_strengths.insert(std::pair<std::string, double>("8Jo", 0.49690438352536087));
    pocket_strengths.insert(std::pair<std::string, double>("48o", 0.3659276700880495));
    pocket_strengths.insert(std::pair<std::string, double>("4Qo", 0.4698255135935799));
    pocket_strengths.insert(std::pair<std::string, double>("59o", 0.4026925953627524));
    pocket_strengths.insert(std::pair<std::string, double>("5Ko", 0.5135494697793553));
    pocket_strengths.insert(std::pair<std::string, double>("QAo", 0.6345468859245883));
    pocket_strengths.insert(std::pair<std::string, double>("8Ao", 0.5826454277547094));
    pocket_strengths.insert(std::pair<std::string, double>("88o", 0.6870874541615735));
    pocket_strengths.insert(std::pair<std::string, double>("3Ts", 0.43615980364516826));
    pocket_strengths.insert(std::pair<std::string, double>("5To", 0.4178012554150827));
    pocket_strengths.insert(std::pair<std::string, double>("TJs", 0.5615141430948419));
    pocket_strengths.insert(std::pair<std::string, double>("7Qs", 0.5268681291266819));
    pocket_strengths.insert(std::pair<std::string, double>("AAo", 0.850266728645107));
    pocket_strengths.insert(std::pair<std::string, double>("KAo", 0.6425529796929611));
    pocket_strengths.insert(std::pair<std::string, double>("2To", 0.39074527301888573));
    pocket_strengths.insert(std::pair<std::string, double>("2Ts", 0.4280542836834884));
    pocket_strengths.insert(std::pair<std::string, double>("9Jo", 0.5169578622816033));
    pocket_strengths.insert(std::pair<std::string, double>("8As", 0.6074437736349765));
    pocket_strengths.insert(std::pair<std::string, double>("9Qo", 0.5378298018149462));
    pocket_strengths.insert(std::pair<std::string, double>("TQo", 0.5580433007437487));
    pocket_strengths.insert(std::pair<std::string, double>("3Qo", 0.46158941128417985));
    pocket_strengths.insert(std::pair<std::string, double>("6As", 0.5786441809984972));
    pocket_strengths.insert(std::pair<std::string, double>("3Jo", 0.42840982457689314));
    pocket_strengths.insert(std::pair<std::string, double>("2Qs", 0.4837269299464179));
    pocket_strengths.insert(std::pair<std::string, double>("59s", 0.4334826870490561));
    pocket_strengths.insert(std::pair<std::string, double>("2As", 0.5558340248962655));
    pocket_strengths.insert(std::pair<std::string, double>("34s", 0.3582719170099962));
    pocket_strengths.insert(std::pair<std::string, double>("6Js", 0.4841845929992229));
    pocket_strengths.insert(std::pair<std::string, double>("5As", 0.5781759766821788));
    pocket_strengths.insert(std::pair<std::string, double>("7Qo", 0.4990318547450182));
    pocket_strengths.insert(std::pair<std::string, double>("JKo", 0.5950154903054434));
    pocket_strengths.insert(std::pair<std::string, double>("78o", 0.4288434422498307));
    pocket_strengths.insert(std::pair<std::string, double>("2Ks", 0.5132763910772038));
    pocket_strengths.insert(std::pair<std::string, double>("57o", 0.37833586281004555));
    pocket_strengths.insert(std::pair<std::string, double>("34o", 0.3215463883403025));
    pocket_strengths.insert(std::pair<std::string, double>("7Js", 0.5019448812381031));
    pocket_strengths.insert(std::pair<std::string, double>("5Ts", 0.45010055718571756));
    pocket_strengths.insert(std::pair<std::string, double>("QKo", 0.6054079003038578));
    pocket_strengths.insert(std::pair<std::string, double>("4To", 0.4080612464717547));
    pocket_strengths.insert(std::pair<std::string, double>("3Ko", 0.4935291535388223));
    pocket_strengths.insert(std::pair<std::string, double>("78s", 0.4550608361237277));
    pocket_strengths.insert(std::pair<std::string, double>("9Ko", 0.5631815797465559));
    pocket_strengths.insert(std::pair<std::string, double>("8To", 0.4779739571838446));
    pocket_strengths.insert(std::pair<std::string, double>("47s", 0.3923241994057445));
    pocket_strengths.insert(std::pair<std::string, double>("48s", 0.4030551514349954));
    pocket_strengths.insert(std::pair<std::string, double>("3Js", 0.4597876071062295));
    pocket_strengths.insert(std::pair<std::string, double>("3Ao", 0.5381746343568943));
    pocket_strengths.insert(std::pair<std::string, double>("8Ko", 0.543634522485433));
    pocket_strengths.insert(std::pair<std::string, double>("8Qo", 0.5210816019137908));
    pocket_strengths.insert(std::pair<std::string, double>("3Ks", 0.5210911597675869));
    pocket_strengths.insert(std::pair<std::string, double>("99o", 0.7164472738928125));
    pocket_strengths.insert(std::pair<std::string, double>("38s", 0.3804215178600877));
    pocket_strengths.insert(std::pair<std::string, double>("8Qs", 0.5446322264849848));
    pocket_strengths.insert(std::pair<std::string, double>("5Js", 0.47680220126307415));
    pocket_strengths.insert(std::pair<std::string, double>("67o", 0.3977783290608892));
    pocket_strengths.insert(std::pair<std::string, double>("8Js", 0.5247295464319979));
    pocket_strengths.insert(std::pair<std::string, double>("JJo", 0.7693362680145555));
    pocket_strengths.insert(std::pair<std::string, double>("69s", 0.45409183285693044));
    pocket_strengths.insert(std::pair<std::string, double>("28s", 0.37471179871019483));
    pocket_strengths.insert(std::pair<std::string, double>("KAs", 0.6605624483043838));
    pocket_strengths.insert(std::pair<std::string, double>("55o", 0.5922441990648256));
    pocket_strengths.insert(std::pair<std::string, double>("56s", 0.40417359494512806));
    pocket_strengths.insert(std::pair<std::string, double>("7To", 0.458181918747753));
    pocket_strengths.insert(std::pair<std::string, double>("39o", 0.37483803089872086));
    pocket_strengths.insert(std::pair<std::string, double>("9To", 0.49967758469602025));
    pocket_strengths.insert(std::pair<std::string, double>("7Ts", 0.48907875926726285));
    pocket_strengths.insert(std::pair<std::string, double>("2Qo", 0.45166950794911237));
    pocket_strengths.insert(std::pair<std::string, double>("TTo", 0.7490572053698064));
    pocket_strengths.insert(std::pair<std::string, double>("7Ks", 0.5591026747195859));
    pocket_strengths.insert(std::pair<std::string, double>("9Ts", 0.5271402369503793));
    pocket_strengths.insert(std::pair<std::string, double>("33o", 0.5292106486091748));
    pocket_strengths.insert(std::pair<std::string, double>("9Js", 0.5395866613418531));
    pocket_strengths.insert(std::pair<std::string, double>("45s", 0.38208122999769045));
    pocket_strengths.insert(std::pair<std::string, double>("6Qo", 0.48956640015924097));
    pocket_strengths.insert(std::pair<std::string, double>("TQs", 0.5794870087717838));
    pocket_strengths.insert(std::pair<std::string, double>("6Ts", 0.46770667236532804));
    pocket_strengths.insert(std::pair<std::string, double>("36s", 0.36955909866057385));
    pocket_strengths.insert(std::pair<std::string, double>("6Ao", 0.5579186923443228));
    pocket_strengths.insert(std::pair<std::string, double>("89s", 0.48581174609452243));
    pocket_strengths.insert(std::pair<std::string, double>("JQs", 0.5896558596864204));
    pocket_strengths.insert(std::pair<std::string, double>("2Ao", 0.5296566537861089));
    pocket_strengths.insert(std::pair<std::string, double>("JKs", 0.6133872565203037));
    pocket_strengths.insert(std::pair<std::string, double>("4Qs", 0.4979161477791615));
    pocket_strengths.insert(std::pair<std::string, double>("79s", 0.4688634320157181));
    pocket_strengths.insert(std::pair<std::string, double>("8Ks", 0.566052508829213));
    pocket_strengths.insert(std::pair<std::string, double>("35s", 0.36660208322983423));
    pocket_strengths.insert(std::pair<std::string, double>("6Ks", 0.5445730992220148));
    pocket_strengths.insert(std::pair<std::string, double>("4As", 0.5743903049727077));
    pocket_strengths.insert(std::pair<std::string, double>("45o", 0.3501563887709001));
    pocket_strengths.insert(std::pair<std::string, double>("23o", 0.2911422491225161));
    pocket_strengths.insert(std::pair<std::string, double>("22o", 0.4948189970109598));
    pocket_strengths.insert(std::pair<std::string, double>("5Qs", 0.5074654132965737));
    pocket_strengths.insert(std::pair<std::string, double>("58s", 0.4196444842038997));
    pocket_strengths.insert(std::pair<std::string, double>("4Ko", 0.5031494148718686));
    pocket_strengths.insert(std::pair<std::string, double>("TKo", 0.5846124828722478));
    pocket_strengths.insert(std::pair<std::string, double>("4Ao", 0.5477801116973476));
    pocket_strengths.insert(std::pair<std::string, double>("2Ko", 0.4832314136471469));
    pocket_strengths.insert(std::pair<std::string, double>("77o", 0.6548067886560893));
    pocket_strengths.insert(std::pair<std::string, double>("TJo", 0.5367009990274954));
    pocket_strengths.insert(std::pair<std::string, double>("66o", 0.6292511735010186));
    pocket_strengths.insert(std::pair<std::string, double>("2Js", 0.44776540017240235));
    pocket_strengths.insert(std::pair<std::string, double>("37o", 0.3383473991946605));
    pocket_strengths.insert(std::pair<std::string, double>("68s", 0.4373854204859838));
    pocket_strengths.insert(std::pair<std::string, double>("37s", 0.3713703261734288));
    pocket_strengths.insert(std::pair<std::string, double>("44o", 0.5619453943679008));
    pocket_strengths.insert(std::pair<std::string, double>("28o", 0.3404739063167176));
    pocket_strengths.insert(std::pair<std::string, double>("2Jo", 0.42025410275840325));
    
    // packet strings
    const std::string new_game("NEWGAME");
    const std::string new_hand("NEWHAND");
    const std::string get_action("GETACTION");
    const std::string hand_over("HANDOVER");
    const std::string request_keyvalues("REQUESTKEYVALUES");
    const std::string true_string("true");
    std::string first_word;
    std::string action;
    
    // game data
    std::string name;
    std::string opponent_name;
    std::string big_blind;
    std::string time_bank;
    int hand_id;
    bool button;
    int pot_size;
    std::string card_one;
    std::string card_two;
    std::string pocket_strength;
    std::string board_cards[5];
    std::string state;
    std::map<int, int> street;
    street.insert(std::pair<int, int>(0, 0));
    street.insert(std::pair<int, int>(3, 0));
    street.insert(std::pair<int, int>(4, 0));
    street.insert(std::pair<int, int>(5, 0));
    
    while (std::getline(stream, line)) {
        std::cout << line << "\n";
        
        std::vector<std::string> packet;
        
        std::size_t start = 0, end = 0;
        while ((end = line.find(" ", start)) != std::string::npos) {
            packet.push_back(line.substr(start, end - start));
            start = end + 1;
        }
        packet.push_back(line.substr(start));
        
        first_word = packet[0];
        
        if (get_action.compare(first_word) == 0) {
            // extract information
            pot_size = atoi(packet[1].c_str());
            int num_board_cards = atoi(packet[2].c_str());
            street[num_board_cards] += 1;
            if (num_board_cards == 5 && state.compare("POSTRIVER") != 0) {
                state = "POSTRIVER";
            } else if (num_board_cards == 4 && state.compare("TURNRIVER") != 0) {
                state = "TURNRIVER";
            } else if (num_board_cards == 3 && state.compare("FLOPTURN") != 0) {
                state = "FLOPTURN";
            }
            int index = 3;
            for (int i = 0; i < num_board_cards; i++) {
                if(board_cards[i].compare("") == 0) {
                    board_cards[i] = packet[index+i];
                }
            }
            index += num_board_cards;
            int num_last_actions = atoi(packet[index].c_str());
            std::string *last_actions = NULL;
            index += 1;
            last_actions = new std::string[num_last_actions];
            for (int i = 0; i < num_last_actions; i++) {
                last_actions[i] = packet[index+i];
            }
            index += num_last_actions;
            int num_legal_actions = atoi(packet[index].c_str());
            std::string *legal_actions = NULL;
            index += 1;
            legal_actions = new std::string[num_legal_actions];
            for (int i = 0; i < num_legal_actions; i++) {
                legal_actions[i] = packet[index+i];
            }
            time_bank = packet.back();
            // logic
            
            // clean up
            delete[] last_actions;
            delete[] legal_actions;
            last_actions = NULL;
            legal_actions = NULL;
            action = "CHECK";
        } else if (new_hand.compare(first_word) == 0) {
            // extract information
            hand_id = atoi(packet[1].c_str());
            button = true_string.compare(packet[2]) == 0;
            card_one = packet[3];
            card_two = packet[4];
            std::map<std::string, double>::iterator it;
            std::string pocket = std::string(1, card_one[0]) + std::string(1, card_two[0]);
            if (card_one[1] == card_two[1]) pocket += "s";
            else pocket += "o";
            it = pocket_strengths.find(pocket);
            if (it == pocket_strengths.end()) pocket = std::string(1, pocket[1]) + std::string(1, pocket[0]) + std::string(1, pocket[2]);
            pocket_strength = pocket_strengths[pocket];
            state = "PREFLOP";
            time_bank = atoi(packet.back().c_str());
            for (int i = 0; i < 5; i++) {
                board_cards[i] = "";
            }
        } else if (hand_over.compare(first_word) == 0) {
            // extract information
            time_bank = atoi(packet.back().c_str());
        } else if (new_game.compare(first_word) == 0) {
            // extract information
            name = packet[1];
            opponent_name = packet[2];
            big_blind = packet[4];
            time_bank = atoi(packet.back().c_str());
        } else if (request_keyvalues.compare(first_word) == 0) {
            action = "FINISH";
        }
        
        stream << action << "\n";
    }
    
    std::cout << "Gameover, engine disconnected.\n";
}
