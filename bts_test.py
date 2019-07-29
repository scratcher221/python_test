import math

class Vote:
    def __init__(self, answer, prediction):
        self.answer = answer
        self.prediction = prediction

def bts(num_answer_options, votes):
    # Check for errors (Total prediction percentage less than or greater than 100):
    # Set a minimum default value for predictions (otherwise geometric mean doesn't get calculated correctly)
    for vote in votes:
        total_prediction_percentage = 0
        for answer in vote.prediction:
            total_prediction_percentage += vote.prediction[answer] / 100
            if vote.prediction[answer] == 0:
                vote.prediction[answer] = 0.1
        if total_prediction_percentage != 1:
            print("Error, total prediction must add up to 100% for each respondent.")
            return False
    # Print all the votes and predictions:
    respondent_index = 0
    for vote in votes:
        print(F"Answer of respondent {respondent_index + 1}: {vote.answer}")
        print(F"Prediction of respondent {respondent_index + 1}:\n")
        for answer in vote.prediction:
            print(F"Answer: {answer}, Percentage: {vote.prediction[answer]}")
        print("")
        respondent_index += 1
    # Calculate the total votes and endorsement frequencies for answer k:
    total_votes = []
    endorsement_frequencies = []
    for i in range(num_answer_options):
        total_votes.append(0)
        endorsement_frequencies.append(0)
    for vote in votes:
        if (vote.answer > num_answer_options or vote.answer < 1):
            print(F"Error. Answer option {vote.answer} does not exist.")
            return False
        total_votes[vote.answer - 1] += 1
    # Print the total votes:
    for i in range(len(total_votes)):
        print(F"Answer {i + 1} has {total_votes[i]} vote(s)")
        endorsement_frequencies[i] = total_votes[i] / len(votes)
        # Set minimum default for endorsement frequencies, to prevent division by zero
        if endorsement_frequencies[i] == 0:
            endorsement_frequencies[i] = 0.001
        print(F"Endorsement frequencies for answer {i + 1}: {round(endorsement_frequencies[i] * 100, 2)}%")
    # Calculate the geometric (and arithmetic for testing) average of predicted frequencies:
    geometric_avg_predicted_frequencies = []
    arithmetic_avg_predicted_frequencies = []
    predicted_frequencies = []
    total_predicted_frequencies = []
    information_scores = []
    for i in range(num_answer_options):
        geometric_avg_predicted_frequencies.append(0)
        arithmetic_avg_predicted_frequencies.append(0)
        total_predicted_frequencies.append(0)
        predicted_frequencies.append(0)
        information_scores.append(0)
    for vote in votes:
        for answer in vote.prediction:
            if (vote.prediction[answer] != 0):
                total_predicted_frequencies[answer - 1] += vote.prediction[answer]
                predicted_frequencies[answer - 1] += math.log10(vote.prediction[answer] / 100)
                arithmetic_avg_predicted_frequencies[answer - 1] += vote.prediction[answer] / 100
    for i in range(len(predicted_frequencies)):
        predicted_frequencies[i] = predicted_frequencies[i] / len(votes)
        arithmetic_avg_predicted_frequencies[i] = arithmetic_avg_predicted_frequencies[i] / len(votes)
        geometric_avg_predicted_frequencies[i] = 10**predicted_frequencies[i]
        # print(F"Geometric average of predictions for answer {i + 1}: {geometric_avg_predicted_frequencies[i]}")
        # print(F"Arithmetic average of predictions for answer {i + 1}: {arithmetic_avg_predicted_frequencies[i]}")
        # print(F"Total predicted frequencies for answer {i + 1}: {total_predicted_frequencies[i]}")
        # Calculate the information scores (log-ratio of actual to predicted endorsement frequencies) for all answers
        # print(F"Calculating information score for answer {i + 1}: {endorsement_frequencies[i]}/{geometric_avg_predicted_frequencies[i]}")
        if (endorsement_frequencies[i] != 0 and geometric_avg_predicted_frequencies[i] != 0):
            information_scores[i] = math.log10(endorsement_frequencies[i]/geometric_avg_predicted_frequencies[i])
        elif (endorsement_frequencies[i] == 0):
            information_scores[i] = -float("inf")
        elif (geometric_avg_predicted_frequencies[i] == 0):
            information_scores[i] = float("inf")
        print(F"The information score for answer {i + 1} is: {information_scores[i]}")
    # Calculate the prediction scores for all respondents
    # Parameter 'alpha' is for tweaking the weight of the prediction penalty
    alpha = 1
    prediction_scores = []
    respondent_scores = []
    respondent_index = 0
    for vote in votes:
        prediction_scores.append(0)
        respondent_scores.append(0)
        for answer in vote.prediction:
            prediction_scores[respondent_index] += endorsement_frequencies[answer - 1] * math.log10((vote.prediction[answer] / 100) / endorsement_frequencies[answer - 1])
        # print(F"Prediction score for respondent {respondent_index + 1}: {prediction_scores[respondent_index]}")
        # Respondent score = information score of their selected answer + the respondent's prediction score
        respondent_scores[respondent_index] = information_scores[vote.answer - 1] + alpha * prediction_scores[respondent_index]
        print(F"Respondent score for respondent {respondent_index + 1}: {respondent_scores[respondent_index]}")
        print(F"Respondent score consists of: Information score: {information_scores[vote.answer - 1]} + Prediction score: {prediction_scores[respondent_index]}")
        respondent_index += 1

    return respondent_scores

    # for i in range(len(arithmetic_avg_predicted_frequencies)):
    #     print(F"Arithmetic average of predictions for answer {i + 1}: {arithmetic_avg_predicted_frequencies[i]}")
    
    
    
    
            
# Let's say there's a multiple choice question with 5 options
# The first argument of the Vote object is the answer that the respondent has chosen (1 - 5)
# The second argument of the Vote object is the prediction that the respondent makes about the empirical distribution of the answer frequencies
prediction1 = { 1: 10, 2: 60, 3: 10, 4: 20, 5: 0 }
prediction2 = { 1: 10, 2: 20, 3: 70, 4: 0, 5: 0 }
prediction3 = { 1: 5, 2: 55, 3: 15, 4: 25, 5: 0 }
prediction4 = { 1: 0, 2: 100, 3: 0, 4: 0, 5: 0 }
prediction5 = { 1: 25, 2: 25, 3: 25, 4: 25, 5: 0 }
prediction6 = { 1: 10, 2: 10, 3: 10, 4 : 70, 5: 0 }
prediction7 = { 1: 10, 2: 10, 3: 80, 4: 0, 5: 0}
v1 = Vote(2, prediction1)
v2 = Vote(3, prediction2)
v3 = Vote(2, prediction3)
v4 = Vote(2, prediction4)
v5 = Vote(2, prediction5)
v6 = Vote(4, prediction6)
v7 = Vote(5, prediction7)
votes = [v1, v2, v3, v4, v5, v6, v7]

bts(5, votes)

