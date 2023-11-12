import numpy as np
from typing import List, Tuple
import random


#I apologize but I don't actually think this implementation is fully functional; when I change values in the raw_scores matrix
# to account for compatability issues, a large, large percentage of the table just turns into 0's. Otherwise, I do think
# the rest of this is correctly implemented
def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    # i might be stupid but the return value seems to be loosely defined for this problem, so I'll just return a list of 5 pairs (lists)
    # where each pair is just a pair of numbers corresponding to people i.e. matches = [[1,2], [3,4], [5,6], [7,8], [9,10]]
    proposers = [1,2,3,4,5,6,7,8,9,10]
    proposers = random.sample(proposers, 5)
    #making recievers the complimentary list to proposers
    recievers = []
    for i in range(10):
        if i not in proposers:
            recievers.append(i)

    #will change values to 0 to accomodate for incompatible gender combinations
    #okay, so after like lots of fiddling around, I still can't seem to understand why so much of the compatability matrix
    # is set to 0... But otherwise, I do think the rest of this implementation is correct?
    scoresCopy = scores.copy()


   # print("reach 1")
    for i in range(len(gender_pref)):

        #nonbinary people should still be able to be matched with other nonbinary people, regardless of the proposer's preferences
        if (gender_id[i] == "Nonbinary"):
            if (gender_pref[i] == "Men"):
                for j in range(len(gender_id)):
                    if (gender_id[j] != "Men" or gender_id[j] != "Nonbinary"):
                        scoresCopy[i][j] = 0

            if (gender_pref[i] == "Women"):
                for j in range(len(gender_id)):
                    if (gender_id[j] != "Women" or gender_id[j] != "Nonbinary"):
                        scoresCopy[i][j] = 0

        else:

            if (gender_pref[i] == "Men"):
                for j in range(len(gender_id)):
                    if (gender_id[j] != "Men"):
                        scoresCopy[i][j] = 0

            if (gender_pref[i] == "Women"):
                for j in range(len(gender_id)):
                    if (gender_id[j] != "Women"):
                        scoresCopy[i][j] = 0


            #Bisexual people should be okay with being matched to anyone so we shouldn't worry about them
            #if (gender_pref[i] == "Bisexual"):

    #now, we will create the preference lists

    proposerPrefDict = {}
    #hi, this is an incredibly inefficient implementation of creating a preference list for each proposer, but because I didn't really
    # want to figure out how to write a sorting algorithm at 2am this is kind of what we're gonna roll with
    #   but basically it works by iterating through each proposer, taking that proposer's individual scores from the compatability matrix
    #   and then sorting based on scores, before searching again through the compatability matrix to see which reciever that score came from
    #   and then putting the recievers, in order, into another list and appending that to the dict.

    #   a more efficient implementation would probably involve different data-type (linked list /nodes?) that allowed us to
    #   reference their compatabiltiy score and who the reciever is at the same time OR we could just work the identity of the reciever, and not just their scores, into the sorting
    #   algorithm
    for proposer in proposers:
        temp = []
        for reciever in recievers:
            temp.append(scoresCopy[proposer-1][reciever-1])
        temp.sort(reverse=True)
        temp2 = []
        for x in range(5):
            for reciever in recievers:
                if temp[x] == scoresCopy[proposer-1][reciever-1]:
                    temp2.append(reciever)
        proposerPrefDict[proposer] = temp2

    recieverPrefDict = {}
    for reciever in recievers:
        temp = []
        for proposer in proposers:
            temp.append(scoresCopy[reciever-1][proposer-1])
        temp.sort(reverse=True)
        temp2 = []
        for x in range(5):
            for proposer in proposers:
                if temp[x] == scoresCopy[reciever-1][proposer-1]:
                    temp2.append(proposer)

        recieverPrefDict[reciever] = temp2



    #i just make copies of arrays cause I don't want any funny buisness happening to our original data, just in case
    freeProposers = proposers.copy()
    freeRecievers = recievers.copy()

    matches = []


    #my implementation of gala-shapley; I actually think it works decently well!
    while len(freeProposers) != 0:

        #w as in 'woman' per the pseudo code of the gala shapley doc
        #we choose a "free man" by just taking the 0-th entry of the freeProposers array lol
        w = proposerPrefDict[freeProposers[0]][0]
        if w in freeRecievers:
            matches.append([freeProposers[0], w])

            #we need to remove the freeProposer after they get matched
            freeProposers.pop(0)
            freeRecievers.remove(w)
        else:
            #wMatch is the current match of w (since they are currently taken)
            #wMatch set to -1 until we actually figure what number person they are
            wMatch = -1
            for pair in matches:
                if pair[1] == w:
                    wMatch = pair[0]

            #dictionary black magic --- yea now that im reading this several hours later, this code could be a lot more readable
            # if i just stored some of these values in variables first lol
            # but basically we're just comparing the compatability with w for freeProposers[0] and wMatch
            if recieverPrefDict[w].index(freeProposers[0]) > recieverPrefDict[w].index(wMatch):
                matches.remove([wMatch, w])
                matches.append([freeProposers[0], w])
                freeProposers.append(wMatch)
                freeProposers.pop(0)
            else:
                proposerPrefDict[freeProposers[0]].pop(0)


    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as
        "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    #yea, way too much of this is turned to 0's 
    print(scoresCopy)
    return matches


if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)

print(gs_matches)