import numpy as np
import pandas as pd
import os
from scipy.io.wavfile import write


def trim_pkl(path, new_file_name):
    print("start trimming")
    data = pd.read_pickle(path)
    coughs = data['cough']
    length = len(data['cough'][0])

    for idx, c in enumerate(coughs):
        print(idx)
        trimmed = np.trim_zeros(c)
        padded = np.pad(trimmed, (0, length - len(trimmed)), 'constant')
        data['cough'][idx] = padded
    data.to_pickle(new_file_name)
    print('end trimming')
    return data


def resampling(path, reduction_ratio, new_file_name):
    print('start resampling')
    data = pd.read_pickle(path)
    coughs = data['cough']
    length = len(data['cough'][0])

    for idx, c in enumerate(coughs):
        print(idx)
        reduced = c[::reduction_ratio]
        data['cough'][idx] = reduced
    data.to_pickle(new_file_name)
    print('end resampling')
    return data


def _convert_back_to_wave(np_cough, path, new_name, sampling_rate):
    max_int16 = 2 ** 15
    np_cough = np_cough * max_int16
    write(path + '/' + new_name + '.wav', sampling_rate, np_cough.astype(np.int16))


def convert_pkl_to_wav(data, path, sampling_rate):
    coughs = data['cough']
    names = data['uuid']
    for i, cough in enumerate(coughs):
        _convert_back_to_wave(cough, path, names[i], sampling_rate)


# trim_pkl('output_covid.pkl', 'covid_trimmed.pkl')
# data_resampled = resampling('covid_trimmed.pkl', 4, 'covid_reduced.pkl')
# resampling('healthy_trimmed.pkl', 4, 'healthy_reduced.pkl')
# resampling('symptomatic_trimmed.pkl', 4, 'symptomatic_reduced.pkl')
# ===========

original_sampling_rate = 48000
reduced_sampling_rate = 12000  # 48000 / 4

# Covid
# data = pd.read_pickle('covid_trimmed.pkl')
# convert_pkl_to_wav(data, 'trimmed/covid_trimmed', original_sampling_rate)
# convert_pkl_to_wav(data, 'trimmed/covid_reduced', reduced_sampling_rate)

# Symptomatic
# data = pd.read_pickle('symptomatic_trimmed.pkl')
# convert_pkl_to_wav(data, 'trimmed/symptomatic_trimmed', original_sampling_rate)
data = pd.read_pickle('symptomatic_reduced.pkl')
convert_pkl_to_wav(data, 'trimmed/symptomatic_reduced', reduced_sampling_rate)

# Healthy
# data = pd.read_pickle('healthy_trimmed.pkl')
# convert_pkl_to_wav(data, 'trimmed/healthy_trimmed', original_sampling_rate)
data = pd.read_pickle('healthy_reduced.pkl')
convert_pkl_to_wav(data, 'trimmed/healthy_reduced', reduced_sampling_rate)
