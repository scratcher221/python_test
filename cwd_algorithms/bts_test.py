import math
from vote import Vote

def bts(num_answer_options, votes):
    number_of_respondents = len(votes)
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
        print(F"Geometric average of predictions for answer {i + 1}: {geometric_avg_predicted_frequencies[i]}")
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

    # Generate answer matrices to be able to filter respondents
    answer_matrix = []
    for i in range(number_of_respondents):
	    answer_matrix.append([])
	    for j in range(num_answer_options):
		    answer_matrix[i].append(0)
    for i in range(number_of_respondents):
	    answer_matrix[i][votes[i].answer - 1] = 1

    # Select the "best" answer according to LST (least surprised by the truth) principle:
    sum_respondent_scores_answer = []
    lst_value = []
    for k in range(num_answer_options):
        lst_value.append(0)
        sum_respondent_scores_answer.append(0)
    for k in range(num_answer_options):
        for r in range(number_of_respondents):
            sum_respondent_scores_answer[k] += answer_matrix[r][k] * respondent_scores[r]
    for k in range(num_answer_options):
        lst_value[k] = 1 / (number_of_respondents * endorsement_frequencies[k]) * sum_respondent_scores_answer[k]
        print(F"LST value for answer {k + 1} is: {lst_value[k]}")



    return respondent_scores, information_scores

    # for i in range(len(arithmetic_avg_predicted_frequencies)):
    #     print(F"Arithmetic average of predictions for answer {i + 1}: {arithmetic_avg_predicted_frequencies[i]}")
    
    
            
# Test the implementation with the question: Is Philadelphia the capital of Pennsylvania, yes (1) or no (2)?
# 11 vote no, 22 vote yes

# Participants who voted "no" (correct answer):
p1 = {1: 20, 2: 80}
p2 = {1: 40, 2: 60}
p3 = {1: 60, 2: 40}
p4 = {1: 60, 2: 40}
p5 = {1: 60, 2: 40}
p6 = {1: 70, 2: 30}
p7 = {1: 80, 2: 20}
p8 = {1: 80, 2: 20}
p9 = {1: 80, 2: 20}
p10 = {1: 90, 2: 10}
p11 = {1: 90, 2: 10}

# Participants who voted "yes" (incorrect answer):
# Predictions for "yes": 60: 1, 70: 4, 80: 7, 90: 10
p12 = {1: 60, 2: 40}
p13 = {1: 70, 2: 30}
p14 = {1: 70, 2: 30}
p15 = {1: 70, 2: 30}
p16 = {1: 70, 2: 30}
p17 = {1: 80, 2: 20}
p18 = {1: 80, 2: 20}
p19 = {1: 80, 2: 20}
p20 = {1: 80, 2: 20}
p21 = {1: 80, 2: 20}
p22 = {1: 80, 2: 20}
p23 = {1: 80, 2: 20}
p24 = {1: 90, 2: 10}
p25 = {1: 90, 2: 10}
p26 = {1: 90, 2: 10}
p27 = {1: 90, 2: 10}
p28 = {1: 90, 2: 10}
p29 = {1: 90, 2: 10}
p30 = {1: 90, 2: 10}
p31 = {1: 90, 2: 10}
p32 = {1: 90, 2: 10}
p33 = {1: 90, 2: 10}

# Votes
v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11 = Vote(2, p1), Vote(2, p2), Vote(2, p3), Vote(2, p4), Vote(2, p5), Vote(2, p6), Vote(2, p7), Vote(2, p8), Vote(2, p9), Vote(2, p10), Vote(2, p11)
v12, v13, v14, v15, v16, v17, v18, v19, v20 = Vote(1, p12), Vote(1, p13), Vote(1, p14), Vote(1, p15), Vote(1, p16), Vote(1, p17), Vote(1, p18), Vote(1, p19), Vote(1, p20)
v21, v22, v23, v24, v25, v26, v27, v28, v29 = Vote(1, p21), Vote(1, p22), Vote(1, p23), Vote(1, p24), Vote(1, p25), Vote(1, p26), Vote(1, p27), Vote(1, p28), Vote(1, p29)
v30, v31, v32, v33 = Vote(1, p30), Vote(1, p31), Vote(1, p32), Vote(1, p33)
votes = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33]

bts(2, votes)

