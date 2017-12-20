from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize

import matplotlib.pyplot as plt
from itertools import cycle
from scipy import interp

import numpy as np
import pandas as pd

# Open csv files with training and test data
df = pd.read_csv('full_waypoint_info.csv')
#df = df[['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees', 'action']].dropna()
df = df[['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees', 'wind_dir', 'wind_speed', 'wind_gusts', 'visib',
	'pressure', 'remaining_time', 'remaining_distance', 'is_avg_speed_bigger', 'action']].dropna()

df_size = df['action'].count()

action_array = np.array(df['action'])

print(action_array) #245509

#df_to_normalize = df[['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees']]
df_to_normalize = df[['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees', 'wind_dir', 'wind_speed', 'wind_gusts', 'visib',
	'pressure', 'remaining_time', 'remaining_distance', 'is_avg_speed_bigger']]

df_size = df_to_normalize['altitude'].count()


# Normalize data
data = np.array(df_to_normalize.as_matrix()).astype(np.float)
max_array = np.max(data, axis=0)
min_array = np.min(data, axis=0)
max_array_size = len(max_array)

for i in range(data.shape[0]):
    for j in range(max_array_size):
        data[i][j] = (data[i][j] - min_array[j]) / max_array[j]

# Split data on train and test and then save data to file
res_df = pd.DataFrame(data, columns=['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees', 'wind_dir', 'wind_speed', 'wind_gusts', 'visib',
	'pressure', 'remaining_time', 'remaining_distance', 'is_avg_speed_bigger'])
#res_df = pd.DataFrame(data, columns=['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees'])
res_df_size = res_df['altitude'].count()
res_df['action'] = action_array

res_df = res_df.sort_values(['action'])
res_df.index = np.array(range(df_size))

matrix = res_df.as_matrix()

train0 = matrix[:59149, :]
train1 = matrix[78865 : 189141, :]
train2 = matrix[225899 : 240607, :]
train_and_target = np.vstack((train0, train1))
train_and_target = np.vstack((train_and_target, train2))

np.random.shuffle(train_and_target)
print(train_and_target.shape[0])

train = train_and_target[:, :-1]
target_train = train_and_target[:, -1]

target_train = label_binarize(target_train, classes=[0, 1, 2])

test0 = matrix[59149 : 78865, :]
test1 = matrix[189141 : 225899, :]
test2 = matrix[240607 : 245509, :]
test_and_target = np.vstack((test0, test1))
test_and_target = np.vstack((test_and_target, test2))

np.random.shuffle(test_and_target)
print(test_and_target.shape[0])

train_and_test = np.vstack((train_and_target, test_and_target))
data_df = pd.DataFrame(train_and_test, columns=['altitude', 'groundspeed', 'latitudedegrees', 'longitudedegrees', 'wind_dir', 'wind_speed', 'wind_gusts', 'visib',
	'pressure', 'remaining_time', 'remaining_distance', 'is_avg_speed_bigger', 'action'])
data_df.to_csv("plane_dataset.csv")