from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, precision_score
from sklearn.preprocessing import label_binarize

import matplotlib.pyplot as plt
from itertools import cycle
from scipy import interp

import numpy as np
import pandas as pd

# Open csv files with training and test data
df = pd.read_csv('plane_dataset.csv')
matrix = df.as_matrix()

n_samples = matrix.shape[0]
delimeter = 0.75

train = matrix[:int(n_samples * delimeter), :-1]
target_train = matrix[:int(n_samples * delimeter), -1]
target_train = label_binarize(target_train, classes=[0, 1, 2])

test = matrix[int(n_samples * delimeter):, :-1]
target_test = matrix[int(n_samples * delimeter):, -1]
target_test = label_binarize(target_test, classes=[0, 1, 2])

print(test.shape[0])
print(train.shape[0])


n_classes = target_test.shape[1]

print('Fitting RandomForestClassifier...')

#Start random forest algorythm
rf = RandomForestClassifier(n_estimators=100)

#Create random forest using data from train matrix 
rf.fit(train, target_train)

print('Predicting values for test...')

#Try to predict result on test data
y = rf.predict(test)
y_first = y[:, 0]
y_second = y[:, 1]
y_third = y[:, 2]

target_first = target_test[:, 0]
target_second = target_test[:, 1]
target_third = target_test[:, 2]

tp = 0
fp = 0
fn = 0
tn = 0

for i in range(y.shape[0]):
	if (y_third[i] == target_third[i]) and (target_third[i] == 1):
		tp = tp + 1
	elif (y_third[i] == target_third[i]) and (target_third[i] == 0):
		tn = tn + 1
	elif (y_third[i] != target_third[i]) and (target_third[i] == 1):
		fn = fn + 1
	elif (y_third[i] != target_third[i]) and (target_third[i] == 0):
		fp = fp + 1

print(y.shape[0])
print(tp)
print(tp + tn)
print(tp + fn)
print(tp + fp)

print("Precision:")
print(tp * 100.0 / (tp + fp))
print("Recall:")
print(tp * 100.0 / (tp + fn))

exit(0)


y_score = rf.predict_proba(test)
first_class = y_score[0]
second_class = y_score[1]
third_class = y_score[2]

print(y_score)
print("Second class: ")
print(second_class)
print("Third class: ")
print(third_class)

size = third_class.shape[0]

print('Drawing ROC-curves...')

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
precision = dict()
roc_auc = dict()

for i in range(n_classes):
	if i == 0:
		fpr[i], tpr[i], _ = roc_curve(target_test[:, i], first_class[:, 1])
		precision[i] = precision_score(target_test[:, i], first_class[:, 1])
	elif i == 1:
		fpr[i], tpr[i], _ = roc_curve(target_test[:, i], second_class[:, 1])
		precision[i] = precision_score(target_test[:, i], second_class[:, 1])
	elif i == 2:
		fpr[i], tpr[i], _ = roc_curve(target_test[:, i], third_class[:, 1])
		precision[i] = precision_score(target_test[:, i], third_class[:, 1])
	roc_auc[i] = auc(fpr[i], tpr[i])
exit(0)

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
for i, color in zip(range(n_classes), colors):
	if i == 0:
		plt.plot(fpr[i], tpr[i], color=color,
             label='Speed increase / not increase (AUC = {1:0.2f})'
             ''.format(i, roc_auc[i]))
	elif i == 1:
		plt.plot(fpr[i], tpr[i], color=color,
             label='Speed decrease / not decrease (AUC = {1:0.2f})'
             ''.format(i, roc_auc[i]))
	elif i == 2:
		plt.plot(fpr[i], tpr[i], color=color,
             label='Speed constancy / inconstancy (AUC = {1:0.2f})'
             ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-curves')
plt.legend(loc="lower right")
plt.show()