import json
from math import sqrt


# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den
    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def calculate_similar_items(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    c = 0
    for item in prefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print("%d / %d" % (c, len(prefs)))
        # Find the most similar items to this one
        scores = top_matches(prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(prefs, item_match, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        try:
            # Loop over items similar to this one
            for (similarity, item2) in item_match[item]:
                # Ignore if this user has already rated this item
                if item2 in userRatings: continue
                # Weighted sum of rating times similarity
                scores.setdefault(item2, 0)
                scores[item2] += similarity * rating
                # Sum of all the similarities
                totalSim.setdefault(item2, 0)
                totalSim[item2] += similarity
        except KeyError:
            print("Missing Key %s" % (item))

    # Divide each total score by total weighting to get an average
    # TODO avoid double lookups
    rankings = [(score / totalSim[item], item) for item, score in scores.items() if totalSim[item] != 0]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


user_dict = {}
business_dict = {}

with open('/home/vicky/Documents/it/notes/AI/UW/Project/data/review.json') as f:
    for line in f:
        line = json.loads(line)
        user = str(line['user_id'])
        business = str(line['business_id'])
        rate = line['stars']

        if business not in business_dict:
            business_dict[business] = {}
        business_dict[business][user] = rate

        if user not in user_dict:
            user_dict[user] = {}
        user_dict[user][business] = rate

        # for key, value in user_dict.items():
        # print("Key : %s, Value: %s"% (key,value))
# for key, values in items_similar.items():
#     for i in range(len(values)):
#         if values[i][0] > 0.5:
#             print("Key : %s, Value : %s"% (values[i][0], values[i][1]))
# for j in range(len(values[i])):
#     print(values[i][j])

# bus_6nnI3DfHn-DTd6tWnZu7Jg
users_similar = calculate_similar_items(user_dict)
print(get_recommended_items(business_dict, users_similar, 'bus_F1tOtPzcsQk8PqNOatVsCg'))

# usr_zsZBYWYEmLLs81_f-HHM8w
# buss_similar = calculate_similar_items(business_dict)
# print(get_recommended_items(user_dict, buss_similar, 'usr_zsZBYWYEmLLs81_f-HHM8w'))

