import numpy as np
import pandas as pd


# Read data from flightplan
data = pd.read_csv('primary_data/train/training_matrix.csv')
number_of_notes = data['received'].count()

index_array = np.array(data.index).astype(int)
data['index'] = index_array

# Select notes with a 3-minute period
data = data[data['index'] % 3 == 0]
new_number_of_notes = data['received'].count()
data.index = np.array(range(new_number_of_notes))

# Prepare null array for actions
actions = np.zeros(new_number_of_notes)

# Update action column
for i in range(new_number_of_notes - 1):
	if data['callsign'][i] == data['callsign'][i + 1]:
		if data['groundspeed'][i] < data['groundspeed'][i + 1]:
			actions[i] = 0
		elif data['groundspeed'][i] > data['groundspeed'][i + 1]:
			actions[i] = 1
		else:
			actions[i] = 2
	else:
		actions[i] = 3

actions[new_number_of_notes - 1] = 3

data['action'] = actions
data = data[data['action'] != 3]
result_number_of_notes = data['received'].count()
data.index = np.array(range(result_number_of_notes))

data.to_csv("primary_data/delta3_training_matrix.csv")
