import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('metadata_compiled.csv')

d_symptomatic = data[data['status'] == 'symptomatic']
d_healthy = data[data['status'] == 'healthy']
d_covid = data[data['status'] == 'COVID-19']
d_male = data[data['gender'] == 'male']
d_female = data[data['gender'] == 'female']
d_resp_true = data[data['respiratory_condition'] == True]
d_resp_false = data[data['respiratory_condition'] == False]
d_pain_true = data[data['fever_muscle_pain'] == True]
d_pain_false = data[data['fever_muscle_pain'] == False]



# ==========================================================
# Creates a figure of 4 subplots in a 2 by 2 grid
figure, axis = plt.subplots(2, 3, figsize=(13, 10))
# Set the padding
figure.tight_layout(pad=3.0)
# ==========================================================

# Pie chart - Num of Samples
total_num = data.shape[0]
sym_perc = d_symptomatic.shape[0] / total_num
cov_perc = d_covid.shape[0] / total_num
healthy_prec = d_healthy.shape[0] / total_num
unusable = 1 - (sym_perc + cov_perc + healthy_prec)
y = np.array([sym_perc, cov_perc, healthy_prec, unusable])
labels = ['symptomatic', 'covid', 'healthy', 'unusable']
axis[0, 0].pie(y, labels=labels, explode=[0, 0.2, 0, 0], autopct='%1.0f%%')
axis[0, 0].set_title("Pie Chart of 27550 Samples ")

# Pie chart - Gender
total_num = d_male.shape[0] + d_female.shape[0]
male_perc = d_male.shape[0] / total_num
female_perc = d_female.shape[0] / total_num
y = np.array([male_perc, female_perc])
labels = ['males', 'females', ]
axis[0, 2].pie(y, labels=labels, autopct='%1.0f%%')
axis[0, 2].legend(["10418", '5700'], title='Num Samples')
axis[0, 2].set_title("Gender")

# Histogram of Age Distribution
axis[1, 0].hist(data.loc[:, 'age'])
axis[1, 0].set_xlabel('age')
axis[1, 0].set_ylabel('num of samples')
axis[1, 0].legend(["36.8"], title='Avg Age')
axis[1, 0].set_title("Histogram of Age Distribution")

# Pie chart - Respiratory Condition
total_num = d_resp_true.shape[0] + d_resp_false.shape[0]
true_perc = d_resp_true.shape[0] / total_num
false_perc = d_resp_false.shape[0] / total_num
y = np.array([true_perc, false_perc])
labels = ['Yes', 'No', ]
axis[0, 1].pie(y, labels=labels, autopct='%1.0f%%', colors=['cornflowerblue', 'pink'])
axis[0, 1].legend(["2821", '13403'], title='Num Samples')
axis[0, 1].set_title("Respiratory Condition?")

# Pie chart - fever_muscle_pain
total_num = d_pain_true.shape[0] + d_pain_false.shape[0]
true_perc = d_pain_true.shape[0] / total_num
false_perc = d_pain_false.shape[0] / total_num
y = np.array([true_perc, false_perc])
labels = ['Yes', 'No', ]
axis[1, 1].pie(y, labels=labels, autopct='%1.0f%%', colors=['cornflowerblue', '#9AA0A8'])
axis[1, 1].legend(["1928", '14296'], title='Num Samples')
axis[1, 1].set_title("Muscle Pain?")


# Pie chart - Number of Segmented Samples
total_num = 14081 + 5263 + 40592
sym_perc = 14081 / total_num
cov_perc = 5263 / total_num
healthy_prec = 40592 / total_num
y = np.array([sym_perc, healthy_prec, cov_perc])
labels = ['symptomatic', 'healthy', 'covid']
axis[1, 2].pie(y, labels=labels, explode=[0, 0, 0.2], autopct='%1.0f%%')
axis[1, 2].legend(["2291->14081", '6865->40592', '896->5263'], title='Original->Segmented', loc="lower center")
axis[1, 2].set_title("Number of Segmented Cough Samples")

plt.show()