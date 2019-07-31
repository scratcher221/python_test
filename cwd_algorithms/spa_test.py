from vote import Vote
import math

def spa(num_answer_options, votes):
	number_of_votes = len(votes)
	# Count votes for each answer option
	total_votes = {}
	total_votes_percentage = {}
	arithmetic_mean_answer = {}
	sum_predictions = {}
	for i in range(num_answer_options):
		total_votes[i + 1] = 0
		arithmetic_mean_answer[i + 1] = 0
		sum_predictions[i + 1] = 0
	for vote in votes:
		total_votes[vote.answer] += 1
	for answer in total_votes:
		arithmetic_mean_answer[answer] = total_votes[answer] / number_of_votes
		total_votes_percentage[answer] = (total_votes[answer] / number_of_votes) * 100
		print(F"Answer {answer} has {total_votes[answer]} votes ({round(total_votes_percentage[answer], 2)}%), x_k = {arithmetic_mean_answer[answer]}.")
	print("")
	respondent_index = 0
	for vote in votes:
		print(f"Prediction from respondent {respondent_index + 1}:")
		for answer in vote.prediction:
			if (vote.prediction[answer] == 0):
				vote.prediction[answer] = 0.1
			print(f"Answer: {answer}, Prediction: {vote.prediction[answer]}")
		respondent_index += 1
		
	# Calculate the sum of predictions for each answer
	for vote in votes:
		for answer in vote.prediction:
			sum_predictions[answer] += vote.prediction[answer]
	# Divide by the number of votes (each vote contains exactly one prediction), to get average prediction
	avg_predictions = {}
	for answer in sum_predictions:
		avg_predictions[answer] = sum_predictions[answer] / number_of_votes
	# Calculate the geometric average of predictions:
	geo_avg_predictions = {}
	for i in range(num_answer_options):
		geo_avg_predictions[i + 1] = 0
	for vote in votes:
		for answer in vote.prediction:
			geo_avg_predictions[answer] += math.log10(vote.prediction[answer])
	for i in range(num_answer_options):
		geo_avg_predictions[i + 1] = 10**(geo_avg_predictions[i + 1] / number_of_votes)
	# Print the average predictions for each answer:
	print("")
	print(F"Now printing the average predictions: ")
	for answer in avg_predictions:
		print(F"Answer: {answer}, Average Prediction: {round(avg_predictions[answer], 2)}, Geometric Average Prediction: {round(geo_avg_predictions[answer], 2)}")
		
	# Calculate the difference between average predictions and actual votes for each answer
	diff_predictions = {}
	for answer in total_votes_percentage:
		diff_predictions[answer] = total_votes_percentage[answer] - avg_predictions[answer]
		
	# Print the difference of actual votes (percentage) - average predictions
	print("")
	print(F"Now printing the difference of actual votes - average predictions:")
	for answer in diff_predictions:
		print(F"Answer: {answer}, Actual Votes: {round(total_votes_percentage[answer], 2)}%, Average Prediction: {round(avg_predictions[answer], 2)}%, Difference: {round(diff_predictions[answer], 2)}")
		
	# Get the maximum of the differences
	max_difference_answer = max(diff_predictions, key=lambda key: diff_predictions[key])
	print(F"Surprisingly popular answer is: {max_difference_answer}")

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