from __future__ import division


def print_probs(probs_dict, num_players, card_enum):
    top_str = " ".join(str(x) + y[:5 - (len(str(x)))] for (x,y) in card_enum)

    print "  " + top_str
    for i in xrange(num_players + 1):
        print str(i) + " " + " ".join((str(x)[2:7] if x not in [0,1] else ('!!!!!' if x == 1 else '00000')) for x in probs_dict[i])


def create_probs_dict(num_players):
    probs_dict = {}

    for i in xrange(num_players + 1):
        probs_dict[i] = [1/len(SUSPECTS) for x in SUSPECTS] + \
                        [1/len(ROOMS) for x in ROOMS] + \
                        [1/len(WEAPONS) for x in WEAPONS]

    return probs_dict


def create_card_enum(SUSPECTS, ROOMS, WEAPONS):
    return enumerate(SUSPECTS + ROOMS + WEAPONS)


def error_check_cards_list(user_cards_list):
    for num in user_cards_list:
        if not (0 <= num <= 20):
            print "ERROR: All number must be between 0 and 20"
            sys.exit(1)


def player_def_has_card(probs_dict, player_num, card_num):
    for p in probs_dict.keys():
        if p == player_num:
            probs_dict[p][card_num] = 1
        else:
            probs_dict[p][card_num] = 0

    return probs_dict


def parse_input(user_input):
    as_list = user_input.strip().split()
    user_num = int(as_list[0])
    command = as_list[1]
    cards = [int(x) for x in as_list[2:]]

    return (user_num, command, cards)


def add_to_card_locations(card_locations, user_num, card):
    if card_locations[card] is not None:
        print "ERROR: Card location already known"

    else:
        card_locations[card] = user_num

    return card_locations


def initialise_card_locations(num_cards):
    card_locations = {}
    for i in xrange(num_cards):
        card_locations[i] = None

    return card_locations


def remove_from_maybe_dicts(card, num_players, maybe_have_dict):
    for i in xrange(num_players):
        if card in maybe_have_dict[i]:
            maybe_have_dict[i].remove(card)

def initialise_deffo_have_dict(num_players):
    deffo_have_dict = {}
    for i in xrange(num_players):
        deffo_have_dict[i] = []

    return deffo_have_dict


def initialise_maybe_have_dict(num_players):
    maybe_have_dict = {}
    for i in xrange(num_players):
        maybe_have_dict[i] = []

    return maybe_have_dict


def initialise_dont_have_dict(num_players):
    dont_have_dict = {}
    for i in xrange(num_players):
        dont_have_dict[i] = []

    return dont_have_dict


SUSPECTS = ["Scarlett", "Plum  ", "Peacock", "Green ", "Mustard", "White "]
ROOMS = ["Kitchen", "Ballroom", "Conservatory", "Dining", "Billiard",
         "Library", "Lounge", "Hall  ", "Study "]
WEAPONS = ["Candlestick", "Dagger", "Piper ", "Revolver", "Rope  ", "Spanner"]

num_players = input("Enter number of players: ")

probs_dict = create_probs_dict(num_players)
print_probs(probs_dict, num_players, SUSPECTS, ROOMS, WEAPONS)
