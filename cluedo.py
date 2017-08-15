import sys
import signal

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

    # print recreating input
    for i in xrange(num_players):
        if deffo_have_dict[i]:
            out_str = str(i) + " d "
            for card in deffo_have_dict[i]:
                out_str += str(card) + " "
            print out_str
        if maybe_have_dict[i]:
            out_str = str(i) + " m "
            for card in maybe_have_dict[i]:
                out_str += str(card) + " "
            print out_str
        if dont_have_dict[i]:
            out_str = str(i) + " n "
            for card in dont_have_dict[i]:
                out_str += str(card) + " "
            print out_str


def create_card_enum(SUSPECTS, ROOMS, WEAPONS):
    return list(enumerate(SUSPECTS + ROOMS + WEAPONS))


def valid_user_input(user_input, num_players):
    splat = user_input.strip().split()

    if len(splat) < 3:
        print "ERROR: Input too short"
        return False

    if not splat[0].isdigit():
        print "ERROR: First symbol must be player number"
        return False

    if splat[1] not in ["d", "m", "n"]:
        print "ERROR: Second symbol must be either d, m, or n"
        return False

    if not all(x.isdigit() for x in splat[2:]):
        print "ERROR: Remaining symbols must be card numbers"
        return False

    (user_num, command, cards) = parse_input(user_input)

    if command in ['m', 'n'] and len(cards) != 3:
        print "ERROR: Must have three cards"
        return False

    for card in cards:
        if not (0 <= card <= 20):
            print "ERROR: All card numbers must be between 0 and 20"
            return False

    if not 0 <= user_num <= (num_players - 1):
        print "ERROR: Player number invalid"
        return False


    return True


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
    if not valid_user_input(user_input, num_players):
        return

    (user_num, user_command, cards) = parse_input(user_input)

    if user_command == "d":
        # 'Definitely'
        for card in cards:
            if card not in deffo_have_dict[user_num]:
                deffo_have_dict[user_num].append(card)
                card_locations[card] = user_num
                remove_from_maybe_dicts(card, num_players, maybe_have_dict)
                for i in xrange(num_players):
                    if i != user_num:
                        if card not in dont_have_dict[i]:
                            dont_have_dict[i].append(card)

    elif user_command == "m":
        # 'Maybe'
        number_false_maybes = 0
        for card in cards:
            if len(cards) == 3:
                if card in dont_have_dict[user_num]:
                    number_false_maybes += 1

        if number_false_maybes == (len(cards) - 1):
            for card in cards:
                if card not in dont_have_dict[user_num]:
                    if card not in deffo_have_dict[user_num]:
                        deffo_have_dict[user_num].append(card)
                        card_locations[card] = user_num
                        remove_from_maybe_dicts(card, num_players, maybe_have_dict)
                        for i in xrange(num_players):
                            if i != user_num:
                                if card not in dont_have_dict[i]:
                                    dont_have_dict[i].append(card)

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


def ignore_sigint(signal, frame):
    pass


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

signal.signal(signal.SIGINT, ignore_sigint)

while True:
    try:
        user_input = raw_input("\n > ")
        deal_with_input(user_input, num_players, card_locations, deffo_have_dict, maybe_have_dict, dont_have_dict)

        print_cards(num_players, total_num_cards, card_enum, deffo_have_dict, maybe_have_dict, dont_have_dict)
    except EOFError:
        pass
