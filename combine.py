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


def get_adjusted_odds(udog_line, line, odds):
    if line == udog_line:
        return odds, False

    adjust = (1 - (line / udog_line)) * 1000

    adjusted_odds = odds - adjust
    if adjust > 0 and adjusted_odds < 100:
        adjusted_odds = -100 - (100 - odds + adjust)
    elif adjust < 0 and adjusted_odds > -100:
        adjusted_odds = 100 + (100 + odds - adjust)

    return round(adjusted_odds, 0), True


### test cases for get_adjusted_odds
# assert(get_adjusted_odds(10, 9, 130, "U") == -170)
# assert(get_adjusted_odds(10, 11, -170, "U") == 130)
# print(get_adjusted_odds(10, 9, 130, "O"))
# print(get_adjusted_odds(10, 11, 130, "O"))

sites = ["betrivers", "draftkings", "fanduel", "mgm", "pointsbet"]


def get_average_rotowire(rotowire, udog, udog_line):
    adjusted_odds = []
    adjusted_indices = [False] * len(sites)
    adjusted_sites = []

    rotowire_lines = rotowire[udog_line]
    for i in range(len(sites)):
        site = sites[i]
        line = rotowire_lines[site + "_line"]
        odds = rotowire_lines[site + "_odds"]
        if line is not None and odds is not None:
            adjusted_odd, adjusted = get_adjusted_odds(
                float(udog[udog_line][0]), line, odds
            )
            adjusted_odds.append(adjusted_odd)
            adjusted_indices[i] = adjusted
            adjusted_sites.append(site)
    return (
        average_probability(adjusted_odds),
        adjusted_odds,
        adjusted_indices,
        adjusted_sites,
    )


rotowire_file = open("rotowire_results.json", "r")
udog_file = open("udog_results.json", "r")
rotowire = json.load(rotowire_file)
udog = json.load(udog_file)

### test cases for get_adjusted_linesf
# print(get_average_rotowire(rotowire, udog, "Jalen Brunson U*points"))
# print(get_average_rotowire(rotowire, udog, "Joel Embiid O*assists"))


## get output.txt
output = open("output.txt", "w")

for udog_line in udog:
    if udog_line in rotowire:
        avg_prob, adjusted_odds, adjusted_indices, adjusted_sites = get_average_rotowire(
            rotowire, udog, udog_line
        )
        assert len(adjusted_odds) == len(adjusted_sites)
        line = udog_line + ", " + udog[udog_line][0] + ", " + str(avg_prob) + ", "
        for i in range(len(adjusted_sites)):
            line += adjusted_sites[i] + ": " + str(adjusted_odds[i])
            if adjusted_indices[i]:
                line += "*"
            line += ", "
        output.write(line + "\n")

output.close()
