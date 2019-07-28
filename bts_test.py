class Vote:
    def __init__(self, answer, prediction):
        self.answer = answer
        self.prediction = prediction

def bts(votes):
    respondent_index = 0
    for vote in votes:
        print(F"Answer of respondent {respondent_index + 1}: {vote.answer}")
        print(F"Prediction of respondent {respondent_index + 1}:\n")
        for answer in vote.prediction:
            print(F"Answer: {answer}, Percentage: {vote.prediction[answer]}")
        print("")
        respondent_index += 1
            
# Let's say there's a multiple choice question with 4 options
# The first argument of the Vote object is the answer that the respondent has chosen (1 - 4)
# The second argument is the prediction that the respondent makes about the empirical distribution of the answer frequencies
prediction1 = { 1: 10, 2: 60, 3: 10, 4: 20 }
prediction2 = { 1: 10, 2: 20, 3: 70, 4: 0 }
prediction3 = { 1: 5, 2: 55, 3: 15, 4: 25 }
prediction4 = { 1: 0, 2: 100, 3: 0, 4: 0 }
prediction5 = { 1: 25, 2: 25, 3: 25, 4: 25 }
v1 = Vote(2, prediction1)
v2 = Vote(3, prediction2)
v3 = Vote(2, prediction3)
v4 = Vote(2, prediction4)
v5 = Vote(2, prediction5)
votes = [v1, v2, v3, v4, v5]

bts(votes)

