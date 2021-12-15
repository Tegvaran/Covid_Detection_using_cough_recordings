# import pandas as pd
#
#
# def process_dataset(file):
#     dataset = pd.read_csv('output.csv')
#     dataset.insert(1, 'fever_muscle_pain', '')
#     dataset.insert(1, 'respiratory_condition', '')
#     dataset.insert(1, 'gender', '')
#     dataset.insert(1, 'age', '')
#     dataset.insert(1, 'SNR', '')
#     dataset.insert(1, 'status', '')
#
#     data_main = pd.read_csv('data/metadata_compiled.csv')
#     data_main = data_main[['uuid', 'SNR', 'cough_detected', 'age', 'gender', 'respiratory_condition', 'fever_muscle_pain', 'status']]
#     data_main = data_main[data_main['status'] =='COVID-19']
#     data_main = data_main[data_main['cough_detected'] > 0.15]
#
#     for id in data_main['uuid']:
#         dataset.loc[dataset['uuid'].str.contains(id), 'status'] = data_main[data_main['uuid']==id]['status'].values[0]
#         dataset.loc[dataset['uuid'].str.contains(id), 'SNR'] = data_main[data_main['uuid'] == id]['SNR'].values[0]
#         dataset.loc[dataset['uuid'].str.contains(id), 'age'] = data_main[data_main['uuid'] == id]['age'].values[0]
#         dataset.loc[dataset['uuid'].str.contains(id), 'gender'] = data_main[data_main['uuid'] == id]['gender'].values[0]
#         dataset.loc[dataset['uuid'].str.contains(id), 'respiratory_condition'] = data_main[data_main['uuid'] == id]['respiratory_condition'].values[0]
#         dataset.loc[dataset['uuid'].str.contains(id), 'fever_muscle_pain'] = data_main[data_main['uuid'] == id]['fever_muscle_pain'].values[0]
