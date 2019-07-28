def spa(votes, predictions):
	for answer in votes:
		print(f"Answer: {answer}, Votes: {votes[answer]}")
	print("")
	prediction_index = 0
	for prediction in predictions:
		print(f"Prediction from respondent {prediction_index + 1}:")
		for answer in prediction:
			print(f"Answer: {answer}, Prediction: {prediction[answer]}")
		prediction_index += 1
		
	# Calculate the sum of predictions for each answer
	sum_predictions = {}
	for answer in votes:
		sum_predictions[answer] = 0
	number_of_predictions = 0
	for prediction in predictions:
		number_of_predictions += 1
		for answer in prediction:
			sum_predictions[answer] += prediction[answer]
	# Divide by the number of predictions, to get average prediction
	avg_predictions = {}
	for answer in sum_predictions:
		avg_predictions[answer] = sum_predictions[answer] / number_of_predictions
		
	# Print the average predictions for each answer:
	print("")
	print(F"Now printing the average predictions: ")
	for answer in avg_predictions:
		print(F"Answer: {answer}, Average Predictions: {avg_predictions[answer]}")
		
	# Calculate the difference between average predictions and actual votes for each answer
	diff_predictions = {}
	for answer in votes:
		diff_predictions[answer] = votes[answer] - avg_predictions[answer]
		
	# Print the difference of actual votes - average predictions
	print("")
	print(F"Now printing the difference of actual votes - average predictions:")
	for answer in diff_predictions:
		print(F"Answer: {answer}, Difference: {diff_predictions[answer]}")
		
	# Get the maximum of the differences
	max_difference_answer = max(diff_predictions, key=lambda key: diff_predictions[key])
	print(F"Surprisingly popular answer is: {max_difference_answer}")
			
		
votes = {"yes": 10, "no": 20, "maybe": 40, "i don't know": 30}
prediction1 = {"yes": 20, "no": 20, "maybe": 20, "i don't know": 40}
prediction2 = {"yes": 10, "no": 30, "maybe": 40, "i don't know": 20}
prediction3 = {"yes": 80, "no": 10, "maybe": 5, "i don't know": 5}
predictions = [prediction1, prediction2, prediction3]
spa(votes, predictions)