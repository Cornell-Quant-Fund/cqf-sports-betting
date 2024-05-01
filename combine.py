import json


def american_odds_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)


def average_probability(odds_list):
    probabilities = [american_odds_to_probability(odds) for odds in odds_list]
    avg_prob = sum(probabilities) / len(probabilities)
    return avg_prob


def get_adjusted_odds(udog_line, line, odds, o_or_u):
    adjust = (1 - (line / udog_line)) * 1000

    if o_or_u == "O":
        adjusted_odds = odds + adjust
        if adjust > 0 and adjusted_odds > -100:
            adjusted_odds = 100 + (100 + odds - adjust)
        elif adjust < 0 and adjusted_odds < 100:
            adjusted_odds = -100 - (100 - odds + adjust)
    elif o_or_u == "U":
        adjusted_odds = odds - adjust
        if adjust > 0 and adjusted_odds < 100:
            adjusted_odds = -100 - (100 - odds + adjust)
        elif adjust < 0 and adjusted_odds > -100:
            adjusted_odds = 100 + (100 + odds - adjust)
    else:
        print("Error: o_or_u must be 'O' or 'U'")

    return round(adjusted_odds, 0)


### test cases for get_adjusted_odds
# assert(get_adjusted_odds(10, 9, 130, "U") == -170)
# assert(get_adjusted_odds(10, 11, -170, "U") == 130)


def get_average_rotowire(rotowire, udog, udog_line):
    sites = ["betrivers", "draftkings", "fanduel", "mgm", "pointsbet"]
    adjusted_odds = []
    o_or_u = udog_line.split(" ")[-1][0]

    rotowire_lines = rotowire[udog_line]
    for site in sites:
        line = rotowire_lines[site + "_line"]
        odds = rotowire_lines[site + "_odds"]
        if line is not None and odds is not None:
            adjusted_odds.append(
                get_adjusted_odds(float(udog[udog_line][0]), line, odds, o_or_u)
            )

    return average_probability(adjusted_odds)


rotowire_file = open("rotowire_results.json", "r")
udog_file = open("udog_results.json", "r")
rotowire = json.load(rotowire_file)
udog = json.load(udog_file)

### test cases for get_adjusted_linesf
# print(get_average_rotowire(rotowire, udog, "Jalen Brunson U*points"))


output = open("output.txt", "w")

for udog_line in udog:
    if udog_line in rotowire:
        avg_prob = get_average_rotowire(rotowire, udog, udog_line)
        output.write(udog_line + ", " + udog[udog_line][1] + ", " + str(avg_prob) + "\n")

output.close()
