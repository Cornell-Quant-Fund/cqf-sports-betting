def american_odds_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)


def average_probability(odds_list):
    probabilities = [american_odds_to_probability(odds) for odds in odds_list]
    avg_prob = sum(probabilities) / len(probabilities)
    return avg_prob


# Example usage
american_odds = [+150, -200, +300, -150, +100]
avg_prob = average_probability(american_odds)
print(f"Average probability: {avg_prob:.2%}")