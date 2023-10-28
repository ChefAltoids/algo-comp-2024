#!usr/bin/env python3
import json
import sys
import os

# we will need to use sqrt to calculate cos-similarity
import math

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses




#The below compute_score function only implements cosine similarity -- more complex weighing schemes 
# would require some pre-processing of data to calculate question weights
# I'm unsure if we're encouraged to write code outside of the compute_score method, but here's how I
# might go about it:
#   1. parse the .json data file into a 2D array that will tell us how many students answered 
#   A,B,C,D, or E for each of the 20 questions (it would be 20 by 5 in size) - this will be useful for 
#   understanding the data better
#   2. Make another 2D array that would implement inverse proportion multiplication; a weight is calculated
#   to each question pair in accordance to the proportion of answers (the 2D array made in step 1 will be
#   helpful for this!)

# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    #block of code below used to see if user1 and user2 are compatible in terms of gender/sexual orientation
    preferenceMatch1 = False
    for orientation in user1.preferences:
        if orientation == user2.gender:
            preferenceMatch1 = True
    preferenceMatch2 = False
    for orientation in user2.preferences:
        if orientation == user1.gender:
            preferenceMatch2 = True
    if (not (preferenceMatch1 and preferenceMatch2)):
        return 0
    
    # IF THE GRADES DONT TOUCH THEN THEY DONT TOUCH
    gradeDifference = abs(user1.grad_year - user2.grad_year)
    if (gradeDifference > 1):
        return 0
    
    #cosine similarity implementation
    dotProduct = 0
    #var1 and var2 is just the sum of the squares of entries; sorry I'm not more creative about variable names lol
    var1 = 0 
    var2 = 0
    for i in range(20):
        dotProduct += user1.responses[i] * user2.responses[i]
        var1 += user1.responses[i]**2
        var2 += user2.responses[i]**2

    magnitude1 = math.sqrt(var1)
    magnitude2 = math.sqrt(var2)
        
    cosSim = dotProduct / (magnitude1 * magnitude2)
    return cosSim


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))


print(users)