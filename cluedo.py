def print_cards(num_players, num_cards, cards_enum, deffo_have_dict, maybe_have_dict, dont_have_dict):
    print "  " + " ".join(str(x) + y[:5 - (len(str(x)))] for (x,y) in card_enum)
    for i in xrange(num_players):
        out_str = ""
        for x in xrange(num_cards):
            if x in deffo_have_dict[i]:
                out_str += "  D   "
            elif x in maybe_have_dict[i]:
                out_str += "  M   "
            elif x in dont_have_dict[i]:
                out_str += "  N   "
            else:
                out_str += "  ?   "

        print str(i) + " " + out_str


def create_card_enum(SUSPECTS, ROOMS, WEAPONS):
    return enumerate(SUSPECTS + ROOMS + WEAPONS)


def error_check_cards_list(user_cards_list):
    for num in user_cards_list:
        if not (0 <= num <= 20):
            print "ERROR: All number must be between 0 and 20"
            sys.exit(1)


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


def deal_with_input(user_input, num_players, card_locations, deffo_have_dict, maybe_have_dict, dont_have_dict):
    (user_num, user_command, cards) = parse_input(user_input)
    # error_check_cards_list(user_input_list)

    if user_command == "d":
        # 'Definitely'
        for card in cards:
            if card not in deffo_have_dict[user_num]:
                deffo_have_dict[user_num].append(card)
                card_locations[card] = user_num
                remove_from_maybe_dicts(card, num_players, maybe_have_dict)

    elif user_command == "m":
        # 'Maybe'
        for card in cards:
            if card_locations[card] is not None:
                continue
            if card in maybe_have_dict[user_num]:
                continue
            if card in dont_have_dict[user_num]:
                continue

            if card not in maybe_have_dict[user_num]:
                maybe_have_dict[user_num].append(card)

    elif user_command == "n":
        # 'Not'
        for card in cards:
            if card in maybe_have_dict[user_num]:
                maybe_have_dict.remove(card)

            if card not in dont_have_dict[user_num]:
                dont_have_dict[user_num].append(card)

    else:
        print "ERROR: Invalid command"
        sys.exit(1)


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
total_num_cards = len(SUSPECTS) + len(ROOMS) + len(WEAPONS)

num_players = input("Enter number of players: ")

card_enum = create_card_enum(SUSPECTS, ROOMS, WEAPONS)

card_locations = initialise_card_locations(total_num_cards)

deffo_have_dict = initialise_deffo_have_dict(num_players)
maybe_have_dict = initialise_maybe_have_dict(num_players)
dont_have_dict = initialise_dont_have_dict(num_players)

print_cards(num_players, total_num_cards, card_enum, deffo_have_dict, maybe_have_dict, dont_have_dict)

while True:
    user_input = raw_input("Next (e.g. 2 d 4 or 3 m 5 16): ")
    deal_with_input(user_input, num_players, card_locations, deffo_have_dict, maybe_have_dict, dont_have_dict)

    print_cards(num_players, total_num_cards, card_enum, deffo_have_dict, maybe_have_dict, dont_have_dict)
