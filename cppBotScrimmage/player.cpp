#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include "player.hpp"
#include "SKPokerEval/src/FiveEval.cpp"
#include "SKPokerEval/src/SevenEval.h"

Player::Player() {
}

void Player::run(tcp::iostream &stream) {
    std::string line;
    
    //evaluator
    int hand_rank;
    std::string hand_class;
    const std::string HIGH_CLASS("HIGH"); // high card
    const std::string PAIR_CLASS("PAIR"); // pair
    const std::string TWO_CLASS("TWO"); // two pair
    const std::string THREE_CLASS("THREE"); // three of a kind or better
    
    FiveEval const eval;
    
    const int WORST_PAIR = 1278;
    const int WORST_TWO = 4138;
    const int WORST_THREE = 4996;
    
    /*
     rank < 1278 high card
     rank < 4138 pair
     rank < 4996 two pair
     above three of a kind or better
     */
    
    std::string cards[] = {"As", "Ah", "Ad", "Ac", "Ks", "Kh", "Kd", "Kc", "Qs", "Qh", "Qd", "Qc", "Js", "Jh", "Jd", "Jc", "Ts", "Th", "Td", "Tc", "9s", "9h", "9d", "9c", "8s", "8h", "8d", "8c", "7s", "7h", "7d", "7c", "6s", "6h", "6d", "6c", "5s", "5h", "5d", "5c", "4s", "4h", "4d", "4c", "3s", "3h", "3d", "3c", "2s", "2h", "2d", "2c"};
    
    std::map<std::string, int> deck;
    deck.insert(std::pair<std::string, int>("As", 0));
    deck.insert(std::pair<std::string, int>("Ah", 1));
    deck.insert(std::pair<std::string, int>("Ad", 2));
    deck.insert(std::pair<std::string, int>("Ac", 3));
    deck.insert(std::pair<std::string, int>("Ks", 4));
    deck.insert(std::pair<std::string, int>("Kh", 5));
    deck.insert(std::pair<std::string, int>("Kd", 6));
    deck.insert(std::pair<std::string, int>("Kc", 7));
    deck.insert(std::pair<std::string, int>("Qs", 8));
    deck.insert(std::pair<std::string, int>("Qh", 9));
    deck.insert(std::pair<std::string, int>("Qd", 10));
    deck.insert(std::pair<std::string, int>("Qc", 11));
    deck.insert(std::pair<std::string, int>("Js", 12));
    deck.insert(std::pair<std::string, int>("Jh", 13));
    deck.insert(std::pair<std::string, int>("Jd", 14));
    deck.insert(std::pair<std::string, int>("Jc", 15));
    deck.insert(std::pair<std::string, int>("Ts", 16));
    deck.insert(std::pair<std::string, int>("Th", 17));
    deck.insert(std::pair<std::string, int>("Td", 18));
    deck.insert(std::pair<std::string, int>("Tc", 19));
    deck.insert(std::pair<std::string, int>("9s", 20));
    deck.insert(std::pair<std::string, int>("9h", 21));
    deck.insert(std::pair<std::string, int>("9d", 22));
    deck.insert(std::pair<std::string, int>("9c", 23));
    deck.insert(std::pair<std::string, int>("8s", 24));
    deck.insert(std::pair<std::string, int>("8h", 25));
    deck.insert(std::pair<std::string, int>("8d", 26));
    deck.insert(std::pair<std::string, int>("8c", 27));
    deck.insert(std::pair<std::string, int>("7s", 28));
    deck.insert(std::pair<std::string, int>("7h", 29));
    deck.insert(std::pair<std::string, int>("7d", 30));
    deck.insert(std::pair<std::string, int>("7c", 31));
    deck.insert(std::pair<std::string, int>("6s", 32));
    deck.insert(std::pair<std::string, int>("6h", 33));
    deck.insert(std::pair<std::string, int>("6d", 34));
    deck.insert(std::pair<std::string, int>("6c", 35));
    deck.insert(std::pair<std::string, int>("5s", 36));
    deck.insert(std::pair<std::string, int>("5h", 37));
    deck.insert(std::pair<std::string, int>("5d", 38));
    deck.insert(std::pair<std::string, int>("5c", 39));
    deck.insert(std::pair<std::string, int>("4s", 40));
    deck.insert(std::pair<std::string, int>("4h", 41));
    deck.insert(std::pair<std::string, int>("4d", 42));
    deck.insert(std::pair<std::string, int>("4c", 43));
    deck.insert(std::pair<std::string, int>("3s", 44));
    deck.insert(std::pair<std::string, int>("3h", 45));
    deck.insert(std::pair<std::string, int>("3d", 46));
    deck.insert(std::pair<std::string, int>("3c", 47));
    deck.insert(std::pair<std::string, int>("2s", 48));
    deck.insert(std::pair<std::string, int>("2h", 49));
    deck.insert(std::pair<std::string, int>("2d", 50));
    deck.insert(std::pair<std::string, int>("2c", 51));
    
    // cards
    const std::string CARD_VALUES[] = {"JOKER", "JOKER", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
    
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
    const std::string NEWGAME("NEWGAME");
    const std::string NEWHAND("NEWHAND");
    const std::string GETACTION("GETACTION");
    const std::string HANDOVER("HANDOVER");
    const std::string REQUESTKEYVALUES("REQUESTKEYVALUES");
    const std::string TRUE_STRING("true");
    const std::string PREFLOP("PREFLOP");
    const std::string FLOPTURN("FLOPTURN");
    const std::string TURNRIVER("TURNRIVER");
    const std::string POSTRIVER("POSTRIVER");
    const std::string RAISE("RAISE");
    const std::string BET("BET");
    const std::string CALL("CALL");
    const std::string CHECK("CHECK");
    const std::string DISCARD("DISCARD");
    const std::string FOLD("FOLD");
    const std::string FINISH("FINISH");
    const std::string COLON(":");
    std::string first_word;
    std::string action;
    
    // game data
    std::string name;
    std::string opponent_name;
    int stack_size;
    int big_blind;
    std::string time_bank;
    int hand_id;
    bool button;
    int pot_size;
    int last_pot_size;
    std::string card_one;
    int card_one_value;
    std::string card_two;
    int card_two_value;
    double pocket_strength;
    std::string board_cards[5];
    std::string state;
    std::map<int, int> street;
    street.insert(std::pair<int, int>(0, 0));
    street.insert(std::pair<int, int>(3, 0));
    street.insert(std::pair<int, int>(4, 0));
    street.insert(std::pair<int, int>(5, 0));
    std::string limits[2];
    bool can_raise = false;
    bool can_bet = false;
    bool can_call = false;
    bool can_check = false;
    bool can_discard = false;
    std::string discarded_card;
    int num_hands;
    int bank;
    
    // modular strategy
    int limit_preflop = 50;
    int limit_pair = 20;
    int limit_two = 50;
    
    while (std::getline(stream, line)) {
        
        std::vector<std::string> packet;
        // parse packet
        std::size_t start = 0, end = 0;
        while ((end = line.find(" ", start)) != std::string::npos) {
            packet.push_back(line.substr(start, end - start));
            start = end + 1;
        }
        packet.push_back(line.substr(start));
        
        first_word = packet[0];
        
        if (GETACTION.compare(first_word) == 0) {
            // extract information
            pot_size = atoi(packet[1].c_str());
            int num_board_cards = atoi(packet[2].c_str());
            street[num_board_cards] += 1;
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
            // update hand if discard
            if(can_discard) {
                for (int i = 0; i < num_last_actions; i++) {
                    if (last_actions[i].find(DISCARD) != std::string::npos && last_actions[i].find(name) != std::string::npos) {
                        if(card_one.compare(discarded_card) == 0) {
                            card_one = last_actions[i].substr(11, 2);
                        } else {
                            card_two = last_actions[i].substr(11, 2);
                        }
                    }
                }
            }
            // state change and hand evaluation
            if (num_board_cards == 5 && state.compare(POSTRIVER) != 0) {
                hand_rank = SevenEval::GetRank(deck[card_one], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]], deck[board_cards[3]], deck[board_cards[4]]);
                if (hand_rank < WORST_PAIR) {
                    hand_class = HIGH_CLASS;
                } else if (hand_rank < WORST_TWO) {
                    hand_class = PAIR_CLASS;
                } else if (hand_rank < WORST_THREE) {
                    hand_class = TWO_CLASS;
                } else {
                    hand_class = THREE_CLASS;
                }
                street[num_board_cards] = 0;
                state = POSTRIVER;
            } else if (num_board_cards == 4 && state.compare(TURNRIVER) != 0) {
                hand_rank = eval.GetRank(deck[card_one], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]], deck[board_cards[3]]);
                if (hand_rank < WORST_PAIR) {
                    hand_class = HIGH_CLASS;
                } else if (hand_rank < WORST_TWO) {
                    hand_class = PAIR_CLASS;
                } else if (hand_rank < WORST_THREE) {
                    hand_class = TWO_CLASS;
                } else {
                    hand_class = THREE_CLASS;
                }
                street[num_board_cards] = 0;
                state = TURNRIVER;
            } else if (num_board_cards == 3 && state.compare(FLOPTURN) != 0) {
                hand_rank = eval.GetRank(deck[card_one], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]]);
                if (hand_rank < WORST_PAIR) {
                    hand_class = HIGH_CLASS;
                } else if (hand_rank < WORST_TWO) {
                    hand_class = PAIR_CLASS;
                } else if (hand_rank < WORST_THREE) {
                    hand_class = TWO_CLASS;
                } else {
                    hand_class = THREE_CLASS;
                }
                street[num_board_cards] = 0;
                state = FLOPTURN;
            }
            
            // logic
            // check legal moves; if possible, set min/max bet/raise limits
            action = "";
            can_raise = false;
            can_bet = false;
            can_call = false;
            can_check = false;
            can_discard = false;
            for (int i = 0; i < num_legal_actions; i++) {
                if (legal_actions[i].find(RAISE) != std::string::npos) {
                    can_raise = true;
                    limits[0] = legal_actions[i].substr(6, legal_actions[i].find_last_of(COLON)-6);
                    limits[1] = legal_actions[i].substr(legal_actions[i].find_last_of(COLON)+1);
                } else if (legal_actions[i].find(BET) != std::string::npos) {
                    can_bet = true;
                    limits[0] = legal_actions[i].substr(6, legal_actions[i].find_last_of(COLON)-6);
                    limits[1] = legal_actions[i].substr(legal_actions[i].find_last_of(COLON)+1);
                } else if (legal_actions[i].find(CALL) != std::string::npos) {
                    can_call = true;
                } else if (legal_actions[i].find(CHECK) != std::string::npos) {
                    can_check = true;
                } else if (legal_actions[i].find(DISCARD) != std::string::npos) {
                    can_discard = true;
                }
            }
            int contribution = last_pot_size / 2;
            int opponent_addition = pot_size - last_pot_size;
            if (bank <= (num_hands-hand_id)*1.5) {
                if (state.compare(PREFLOP) == 0) {
                    if (street[0] == 1 && button) {
                        action = CALL;
                    } else {
                        // check pocket to determine play strategy
                        int card_max = std::max(card_one_value, card_two_value);
                        int card_min = std::min(card_one_value, card_two_value);
                        bool all_in = false;
                        if (card_max > 10) {
                            bool same_suit = card_one[1] == card_two[1];
                            switch(card_max) {
                                case 14:
                                    all_in = true;
                                    break;
                                case 13:
                                    if (card_min > 5 || (same_suit && card_min > 2)) {
                                        all_in = true;
                                    }
                                    break;
                                case 12:
                                    if (card_min > 8 || (same_suit && card_min > 5)) {
                                        all_in = true;
                                    }
                                    break;
                                case 11:
                                    if (card_min > 9 || (same_suit && card_min > 7)) {
                                        all_in = true;
                                    }
                                    break;
                                default:
                                    break;
                            }
                        }
                        if (all_in) {
                            if (can_raise) {
                                action = RAISE + COLON + limits[1];
                            } else if (can_call) {
                                action = CALL;
                            }
                        } else if (pocket_strength > 0.55) {
                            if (contribution + opponent_addition > limit_preflop) {
                                if(can_raise) {
                                    action = RAISE + COLON + limits[1];
                                }
                            } else if (can_call) {
                                action = CALL;
                            }
                        }
                    }
                } else if (state.compare(FLOPTURN) == 0 || state.compare(TURNRIVER) == 0) {
                    if (can_discard) {
                        int rank_no_discard = 0;
                        int rank_discard_one = 0;
                        int rank_discard_two = 0;
                        std::string eval_card_one, eval_card_two, eval_card_three;
                        bool loop_one = true;
                        bool loop_two = true;
                        bool loop_three = true;
                        if (state.compare(FLOPTURN) == 0) {
                            for (int i = 0; i < 52; i++) {
                                eval_card_one = cards[i];
                                for (int i = 0; i < num_board_cards; i++) {
                                    if (board_cards[i].compare(eval_card_one) == 0) {
                                        loop_one = false;
                                    }
                                }
                                if (card_one.compare(eval_card_one) == 0) {
                                    loop_one = false;
                                } else if (card_two.compare(eval_card_one) == 0) {
                                    loop_one = false;
                                }
                                if (loop_one) {
                                    for (int j = 0; j < i; j++) {
                                        eval_card_two = cards[j];
                                        for (int i = 0; i < num_board_cards; i++) {
                                            if (board_cards[i].compare(eval_card_two) == 0) {
                                                loop_two = false;
                                            }
                                        }
                                        if (card_one.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        } else if (card_two.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        } else if(eval_card_one.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        }
                                        if (loop_two) {
                                            if (SevenEval::GetRank(deck[eval_card_one], deck[eval_card_two], deck[card_one], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]]) >= WORST_THREE) {
                                                rank_no_discard++;
                                            }
                                            for (std::map<std::string, int>::iterator iter = deck.begin(); iter != deck.end(); iter++) {
                                                eval_card_three = iter->first;
                                                for (int i = 0; i < num_board_cards; i++) {
                                                    if (board_cards[i].compare(eval_card_three) == 0) {
                                                        loop_three = false;
                                                    }
                                                }
                                                if (card_one.compare(eval_card_three) == 0) {
                                                    loop_three = false;
                                                } else if (card_two.compare(eval_card_three) == 0) {
                                                    loop_three = false;
                                                } else if(eval_card_one.compare(eval_card_three) == 0) {
                                                    loop_three = false;
                                                } else if(eval_card_two.compare(eval_card_three) == 0) {
                                                    loop_three = false;
                                                }
                                                if (loop_three) {
                                                    if (SevenEval::GetRank(deck[eval_card_one], deck[eval_card_two], deck[eval_card_three], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]]) >= WORST_THREE) {
                                                        rank_discard_one++;
                                                    }
                                                    if (SevenEval::GetRank(deck[eval_card_one], deck[eval_card_two], deck[eval_card_three], deck[card_one], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]]) >= WORST_THREE) {
                                                        rank_discard_two++;
                                                    }
                                                }
                                                loop_three = true;
                                            }
                                        }
                                        loop_two = true;
                                    }
                                }
                                loop_one = true;
                            }
                            rank_no_discard *= 45;
                        } else {
                            for (std::map<std::string, int>::iterator it = deck.begin(); it != deck.end(); it++) {
                                eval_card_one = it->first;
                                for (int i = 0; i < num_board_cards; i++) {
                                    if (board_cards[i].compare(eval_card_one) == 0) {
                                        loop_one = false;
                                    }
                                }
                                if (card_one.compare(eval_card_one) == 0) {
                                    loop_one = false;
                                } else if (card_two.compare(eval_card_one) == 0) {
                                    loop_one = false;
                                } else if (discarded_card.compare(eval_card_one) == 0) {
                                    loop_one = false;
                                }
                                if (loop_one) {
                                    if (SevenEval::GetRank(deck[eval_card_one], deck[card_one], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]], deck[board_cards[3]]) >= WORST_THREE) {
                                        rank_no_discard++;
                                    }
                                    for (std::map<std::string, int>::iterator ite = deck.begin(); ite != deck.end(); ite++) {
                                        eval_card_two = ite->first;
                                        for (int i = 0; i < num_board_cards; i++) {
                                            if (board_cards[i].compare(eval_card_two) == 0) {
                                                loop_two = false;
                                            }
                                        }
                                        if (card_one.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        } else if (card_two.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        } else if(eval_card_one.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        } else if (discarded_card.compare(eval_card_two) == 0) {
                                            loop_two = false;
                                        }
                                        if (loop_two) {
                                            if (SevenEval::GetRank(deck[eval_card_one], deck[eval_card_two], deck[card_two], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]], deck[board_cards[3]]) >= WORST_THREE) {
                                                rank_discard_one++;
                                            }
                                            if (SevenEval::GetRank(deck[eval_card_one], deck[eval_card_two], deck[card_one], deck[board_cards[0]], deck[board_cards[1]], deck[board_cards[2]], deck[board_cards[3]]) >= WORST_THREE) {
                                                rank_discard_two++;
                                            }
                                        }
                                        loop_two = true;
                                    }
                                }
                                loop_one = true;
                            }
                            int adjust = discarded_card.compare("") == 0 ? 1 : 0;
                            rank_no_discard *= (45 - adjust);
                        }
                        int choice = std::max(rank_no_discard, rank_discard_one);
                        choice = std::max(choice, rank_discard_two);
                        if (choice == rank_discard_one) {
                            action = DISCARD + COLON + card_one;
                            discarded_card = card_one;
                        } else if (choice == rank_discard_two) {
                            action = DISCARD + COLON + card_two;
                            discarded_card = card_two;
                        }
                    } else {
                        if (hand_class.compare(THREE_CLASS) == 0) {
                            if(can_call) {
                                action = CALL;
                            }
                        } else if (hand_class.compare(TWO_CLASS) == 0) {
                            if (contribution + opponent_addition <= limit_two) {
                                if(can_call) {
                                    action = CALL;
                                }
                            }
                        } else if (hand_class.compare(PAIR_CLASS) == 0) {
                            if (contribution + opponent_addition <= limit_pair) {
                                if(can_call) {
                                    action = CALL;
                                }
                            }
                        }
                    }
                } else if (state.compare(POSTRIVER) == 0) {
                    if (hand_class.compare(THREE_CLASS) == 0) {
                        if (can_bet) {
                            action = BET + COLON + limits[1];
                        } else if (can_raise) {
                            action = RAISE + COLON + limits[1];
                        } else if (can_call) {
                            action = CALL;
                        }
                    }
                }
            }
            if (action.compare("") == 0) {
                if (can_check) {
                    action = CHECK;
                } else {
                    action = FOLD;
                }
            }
            // clean up
            last_pot_size = pot_size;
            
            delete[] last_actions;
            delete[] legal_actions;
            last_actions = NULL;
            legal_actions = NULL;
            
            stream << action << "\n";
        } else if (NEWHAND.compare(first_word) == 0) {
            // extract information
            hand_id = atoi(packet[1].c_str());
            button = TRUE_STRING.compare(packet[2]) == 0;
            card_one = packet[3];
            card_two = packet[4];
            card_one_value = std::distance(CARD_VALUES, std::find(CARD_VALUES, CARD_VALUES+15, std::string(1, card_one[0])));
            card_two_value = std::distance(CARD_VALUES, std::find(CARD_VALUES, CARD_VALUES+15, std::string(1, card_two[0])));
            std::map<std::string, double>::iterator it;
            std::string pocket = std::string(1, card_one[0]) + std::string(1, card_two[0]);
            if (card_one[1] == card_two[1]) pocket += "s";
            else pocket += "o";
            it = pocket_strengths.find(pocket);
            if (it == pocket_strengths.end()) pocket = std::string(1, pocket[1]) + std::string(1, pocket[0]) + std::string(1, pocket[2]);
            pocket_strength = pocket_strengths[pocket];
            state = PREFLOP;
            bank = atoi(packet[5].c_str());
            time_bank = packet.back();
            for (int i = 0; i < 5; i++) {
                board_cards[i] = "";
            }
            street[0] = 0;
            hand_rank = 0;
            hand_class = "";
            discarded_card = "";
        } else if (HANDOVER.compare(first_word) == 0) {
            // extract information
            time_bank = packet.back();
        } else if (NEWGAME.compare(first_word) == 0) {
            // extract information
            name = packet[1];
            opponent_name = packet[2];
            stack_size = atoi(packet[3].c_str());
            big_blind = atoi(packet[4].c_str());
            num_hands = atoi(packet[5].c_str());
            time_bank = packet.back();
        } else if (REQUESTKEYVALUES.compare(first_word) == 0) {
            stream << FINISH << "\n";
        }
    }
    
    std::cout << "Gameover, engine disconnected.\n";
}
