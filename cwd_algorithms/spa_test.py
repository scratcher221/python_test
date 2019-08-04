from vote import Vote
import math

def spa(num_answer_options, votes):
	number_of_respondents = len(votes)
	# Count votes for each answer option
	total_votes = []
	total_votes_percentage = []
	arithmetic_mean_answer = []
	# For this implementation of the LST principle, we weight respondents equally (w_j = arithmetic_mean_answer[j])
	weight_answer = []
	sum_predictions = []
	sum_log_predictions = []
	for i in range(num_answer_options):
		total_votes.append(0)
		total_votes_percentage.append(0)
		arithmetic_mean_answer.append(0)
		weight_answer.append(0)
		sum_predictions.append(0)
		sum_log_predictions.append([])
		for j in range(num_answer_options):
			sum_log_predictions[i].append(0)
	for vote in votes:
		total_votes[vote.answer - 1] += 1
	for i in range(len(total_votes)):
		arithmetic_mean_answer[i] = total_votes[i] / number_of_respondents
		if arithmetic_mean_answer[i] == 0:
			arithmetic_mean_answer[i] = 0.001
		weight_answer[i] = arithmetic_mean_answer[i]
		total_votes_percentage[i] = (total_votes[i] / number_of_respondents) * 100
		print(F"Answer {i + 1} has {total_votes[i]} votes ({round(total_votes_percentage[i], 2)}%), x_k = {arithmetic_mean_answer[i]}.")
	print("")
	# Calculate matrix with geometric averages of predictions based on answer of respondent
	# First create a m x m matrix (m answer options), filled with 0s
	geo_avg_prediction_matrix = []
	for i in range(num_answer_options):
		geo_avg_prediction_matrix.append([])
		for j in range(num_answer_options):
			geo_avg_prediction_matrix[i].append(0)

	# Change 0 predictions to 0.1, to prevent domain errors
	respondent_index = 1
	for vote in votes:
		# print(f"Prediction from respondent {respondent_index}:")
		for answer in vote.prediction:
			if (vote.prediction[answer] == 0):
				vote.prediction[answer] = 0.1
			# print(f"Answer: {answer}, Prediction: {vote.prediction[answer]}")
		respondent_index += 1

	# Generate answer matrices to be able to filter predictions by endorsed answer, e.g. answer 3 = [0, 0, 1, 0, 0]
	answer_matrix = []
	for i in range(number_of_respondents):
		answer_matrix.append([])
		for j in range(num_answer_options):
			answer_matrix[i].append(0)
	for i in range(number_of_respondents):
		answer_matrix[i][votes[i].answer - 1] = 1
		# print(F"Answer matrix for respondent {i + 1}: {answer_matrix[i]}")
	# Calculate sum of the logarithms of predictions for answer 1 - 5 of every respondent who chose answer 1 - 5
	for j in range(number_of_respondents):
		# print(F"\nLooking at the vote of respondent {j + 1}:\n")
		for k in range(num_answer_options):
			for l in range(num_answer_options):
				if votes[j].prediction[k + 1] != 0:
					# print(F"Adding {answer_matrix[j][l] * math.log10((votes[j].prediction[k + 1])/100):.5f} to sum_log_predictions[{k}][{l}]...")
					sum_log_predictions[k][l] += answer_matrix[j][l] * math.log10((votes[j].prediction[k + 1])/100)
				else:
					# print(F"Adding {0:.5f} to sum_log_predictions[{k}][{l}]...")
					sum_log_predictions[k][l] += 0
	# for i in range(num_answer_options):
	# 	for j in range(num_answer_options):
			# print(F"The sum of logarithms of predictions for answer {i + 1} of every respondent who chose answer {j + 1} is: {sum_log_predictions[i][j]}\n")

	for i in range(num_answer_options):
		for j in range(num_answer_options):
			if arithmetic_mean_answer[j] != 0:
				# print(F"Arithmetic mean for answer {j + 1} is: {arithmetic_mean_answer[j]}")
				# print(F"Calculating geometric average of predictions of answer {i + 1} of respondents who chose answer {j + 1}: 10^(1/({number_of_respondents} * {arithmetic_mean_answer[j]}) * {sum_log_predictions[i][j]})")
				geo_avg_prediction_matrix[i][j] = 10**(1/(number_of_respondents * arithmetic_mean_answer[j]) * sum_log_predictions[i][j])
				# print(F"The result is: {geo_avg_prediction_matrix[i][j]}")
			else:
				geo_avg_prediction_matrix[i][j] = 0
			print(F"The geometric average of predictions for answer {i + 1} of every respondent who chose answer {j + 1} is: {geo_avg_prediction_matrix[i][j]}")
	print("")
	# Now calculate a weighted sum of the pairwise comparisons of predictions (one sum for each answer option k)
	weighted_sum_predictions = []
	spa_value = []
	for k in range(num_answer_options):
		weighted_sum_predictions.append(0)
		spa_value.append(0)
	for k in range(num_answer_options):
		for j in range(num_answer_options):
			if geo_avg_prediction_matrix[j][k] != 0 and geo_avg_prediction_matrix[k][j] != 0:
				weighted_sum_predictions[k] += weight_answer[j] * math.log10(geo_avg_prediction_matrix[j][k]/geo_avg_prediction_matrix[k][j])

	for k in range(num_answer_options):
		print(F"The weighted sum of the pairwise comparisons of predictions for answer {k + 1} is: {weighted_sum_predictions[k]}")

	# Now calculate the "SPA value" for each answer, and find the maximum
	for k in range(num_answer_options):
		if arithmetic_mean_answer[k] != 0:
			spa_value[k] = math.log10(arithmetic_mean_answer[k]) + weighted_sum_predictions[k]
		else:
			spa_value[k] = 0 + weighted_sum_predictions[k]
		print(F"The SPA value for answer {k + 1} is: {spa_value[k]}")
	
	spa_max = max(spa_value)
	spa = [i for i, val in enumerate(spa_value) if val == spa_max][0]

	print(F"The surprisingly popular answer is: answer {spa + 1}.")

	return spa

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

spa(5, votes)