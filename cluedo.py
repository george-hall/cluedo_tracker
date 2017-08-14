from __future__ import division


def print_probs(probs_dict, num_players, card_enum):
    top_str = " ".join(str(x) + y[:5 - (len(str(x)))] for (x,y) in card_enum)

    print "  " + top_str
    for i in xrange(num_players + 1):
        print str(i) + " " + " ".join(str(x)[2:7] for x in probs_dict[i][0]) + \
              " " + " ".join(str(x)[2:7] for x in probs_dict[i][1]) + \
              " " + " ".join(str(x)[2:7] for x in probs_dict[i][2])


def create_probs_dict(num_players):
    probs_dict = {}

    for i in xrange(num_players + 1):
        probs_dict[i] = [[1/len(SUSPECTS) for x in SUSPECTS],
                         [1/len(ROOMS) for x in ROOMS],
                         [1/len(WEAPONS) for x in WEAPONS]]

    return probs_dict


def create_card_enum(SUSPECTS, ROOMS, WEAPONS):
    return enumerate(SUSPECTS + ROOMS + WEAPONS)


SUSPECTS = ["Scarlett", "Plum  ", "Peacock", "Green ", "Mustard", "White "]
ROOMS = ["Kitchen", "Ballroom", "Conservatory", "Dining", "Billiard",
         "Library", "Lounge", "Hall  ", "Study "]
WEAPONS = ["Candlestick", "Dagger", "Piper ", "Revolver", "Rope  ", "Spanner"]

num_players = input("Enter number of players: ")

probs_dict = create_probs_dict(num_players)
print_probs(probs_dict, num_players, SUSPECTS, ROOMS, WEAPONS)
