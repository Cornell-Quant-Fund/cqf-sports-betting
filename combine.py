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

rotowire_file = open("rotowire_results.json", "r")
udog_file = open("udog_results.json", "r")

rotowire = json.load(rotowire_file)
udog = json.load(udog_file)

lines = ["betrivers", "draftkings", "fanduel", "mgm", "pointsbet"]

# test with one bet
test = "Jalen Brunson U*points"
r = rotowire[test]
u = udog[test]
print(r)
print()
print(u)

# test_odds = []
# for line in lines:
#     test_odds.append(r[line + "_odds"])

# print()


# for (key, value) in rotowire.items():
#     if key in udog:
#         print(rotowire[key])
#         print(udog[key])
