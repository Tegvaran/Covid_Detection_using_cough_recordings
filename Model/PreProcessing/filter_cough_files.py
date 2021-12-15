from os import listdir
from os.path import isfile, join
import shutil, os, os.path
import numpy as np
import pandas as pd

# ========================================
# Get file names and save them to txt
# ========================================
# file_names = [f_name for f_name in listdir("./data/public_dataset") if f_name.endswith("json")]
# file_names_string = ','.join(file_names)
#
# f = open("./data/names_json.txt", "a")
# f.write(file_names_string)
# f.close()
#
# file_names_string = file_names_string.replace(".json", "")
# f = open("names.txt", "a")
# f.write(./data/file_names_string)
# f.close()
# ========================================
# Move all json files to subdirectory
# ========================================
# f = open("./data/names_json.txt", "r")
# file_names = f.read()
# file_names = file_names.split(',')
# for name in file_names:
#     shutil.move('./data/public_dataset/' + name, './data/public_dataset/json')


data = pd.read_csv('data/metadata_compiled.csv')


def move_files_by_status(status, folder_name):
    df_covid = data.loc[data['status'] == status]
    df_covid = df_covid.loc[df_covid['cough_detected'] > 0.15]
    covid_list = df_covid['uuid'].to_list()
    covid_filenames = [f_name for f_name in listdir("./data/public_dataset") if f_name.split('.')[0] in covid_list]
    os.mkdir(folder_name)
    os.mkdir(folder_name + '/json')
    for f_name in covid_filenames:
        if f_name.endswith('.json'):
            shutil.move('./data/public_dataset/' + f_name, folder_name + '/json')
        else:
            shutil.move('./data/public_dataset/' + f_name, folder_name)


print("start")
move_files_by_status('COVID-19', './data/covid')
print("healthy")
move_files_by_status('healthy', './data/healthy')
print("symptomatic")
move_files_by_status('symptomatic', './data/symptomatic')
print("done")


# covid_json = (covid['uuid'] + ".json").to_list()
