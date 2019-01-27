from collections import Counter
import matplotlib.pyplot as plt
'''
Inputs
votes - (dict) name: nr_of_votes
low_threshold - (flot) minimum level (in percents) for recieving a mandate
nr_of_mandates - (int)
'''


def max_key_in_dict(d):
    return max(d, key=(lambda x: d[x]))


def proportional_method(votes, nr_of_mandates, limit,
                        initial_factor=1, plus_factor=1):
    all_votes = sum(v for v in votes.values())
    votes_limit = all_votes * limit / 100.0
    tmp_votes = {k: v for k, v in votes.items() if v > votes_limit}
    factors = {k: initial_factor for k, v in votes.items() if v > votes_limit}
    results = []
    while len(results) < nr_of_mandates:
        # 1. find max keys
        winner = max_key_in_dict(tmp_votes)
        # 2. add winner to list
        results.append((winner, tmp_votes[winner]))
        # 2. increase his factor
        factors[winner] += plus_factor
        # 3. reduce his score
        tmp_votes[winner] = votes[winner] / factors[winner]

    return results


if __name__ == '__main__':
    test_votes = {"Niebiescy": 42.,
                  "Zieloni": 31.,
                  "Żółci": 12.,
                  "Czerwoni": 10.,
                  "Fioletowi": 5.
                  }

    dhondt_result = proportional_method(test_votes, 10, 0, 1, 1)
    saint_result = proportional_method(test_votes, 10, 0, 1, 2)

    dhondt_dict = dict(Counter(r[0] for r in dhondt_result))
    saint_dict = dict(Counter(r[0] for r in saint_result))

    print("D'Hondt results:\n{}\n".format(dhondt_dict))
    print("Saint-Lague results:\n{}\n".format(saint_dict))
