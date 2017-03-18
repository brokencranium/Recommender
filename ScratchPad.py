import json

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

user_dict = {}
business_dict = {}

# {'749EpR01CQCa-6BEtFZtNQ': {'Ulu3wyEJCry7MLhAK3lsUw': 5, '2y-Fvlur19M9FGOZ4aWDtg': 5, 'NBu6NdpVHeqyFNy2OGs9YA': 5,
#                                          '9-p_Grd9pjB8vUFSMK96hg': 5, '4TOydrfx1__SgB-pFvXVCg': 5, 'deL6e_z9xqZTIODKqnvRXQ': 5,
#                                          'IUMZPb307ORS9YcWb6xYMw': 1, 'BoA83SDJI9HV3lJzFs8laQ': 4, 'U4INQZOPSUaj8hMjLlZ3KA': 4,
#                                          '9cGVREDE62j47aSVlxHhjw': 5, 'Ii1PkdRpONUNwKC3lmhl1A': 4, 'EZzV8WIUGWJ7D-e5E7XdjQ': 5,
#                                          'BRN_UPViHXJ3DtZGklmdqw': 4, 'Bj_MarPEKBe2xN12YimekQ': 4, 'q5afJ8gTV5TPEOkzyeJ_WQ': 5},
#              '-tLxryf1OpzVP9OSrznprg': {'OrbBDK-XKfVeIei4t0T0Hg': 5, 'b1Qf5tcu5R-kySnNrFPYew': 5, 'GS3dVZYhg41LoTNAXWSoUw': 5,
#                                         'IUMZPb307ORS9YcWb6xYMw': 1, 'BoA83SDJI9HV3lJzFs8laQ': 4, 'U4INQZOPSUaj8hMjLlZ3KA': 4,
#                                          'cD35x9Q9ARsJkD5PQfyJOA': 5},
#              '3EjjtHEFdTZST55js1A18A': {'VBmnuo4omy2fWiHmh6yOqw': 5, '3iUl2fA53QTpuEow-7VCUA': 2, '934vscqFOlHw2LZN_uFWuw': 1,
#                                          '8Y4G2QNIjiwKvj3hE9fSIA': 3, 'uLQvIvCSPrj5yIq530xBmA': 1, 'PJS8jssQ-k7avg3_77OhUQ': 5,
#                                         'dXzlXoZFWiwqy6BkrwlixA': 5,'BoA83SDJI9HV3lJzFs8laQ': 4, 'U4INQZOPSUaj8hMjLlZ3KA': 4}
#              }


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
        if item in prefs[p2]: si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

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
    if den == 0: return 0

    r = num / den

    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

def calculateSimilarItems(prefs,n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result={}
    # Invert the preference matrix to be item-centric
    # itemPrefs=transformPrefs(prefs)
    c=0
    for item in prefs:
        # Status updates for large datasets
        c+=1
        if c%100==0: print("%d / %d" % (c,len(prefs)))
        # Find the most similar items to this one
        scores=top_matches(prefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result


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


#print(calculateSimilarItems(user_dict))

# print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
# print(sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))
# print(topMatches(critics, 'Lisa Rose'))
#print(get_recommendations(critics, 'Toby', similarity=sim_distance)[0:25])
# print(calculateSimilarItems(critics))

# for key, values in business_dict.items():
#     print("Key: %s, Value: %s "% (key, values))
#     if isinstance(values,dict):
#         for user, rating in values.items():
#             print("User Id : %s Rating : %d"% (user,  rating))

# print(business_dict.get('bus_0MVFN6z4GyPgFpGjJY-sew'))
# print(sim_distance(business_dict, 'bus_0MVFN6z4GyPgFpGjJY-sew', 'bus_-6hVnjeCvU_ImnQEJyrGrw'))

itemsin = calculateSimilarItems(critics)
print(get_recommendations(critics,itemsin,'Toby'))