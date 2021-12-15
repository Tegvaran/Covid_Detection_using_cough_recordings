import pandas as pd
from scipy.io.wavfile import write
import numpy as np

sampling_rate = 48000
file = 'output_covid.pkl'
output_path = '/data/covid/segmented'
data = pd.read_pickle(file)
names = data['uuid']
coughs = data['cough']


def convert_back_to_wave(np_cough, path, new_name):
    max_int16 = 2 ** 15
    np_cough = np_cough * max_int16
    write(path + '/' + new_name + '.wav', sampling_rate, np_cough.astype(np.int16))


for i, cough in enumerate(coughs):
    convert_back_to_wave(cough, output_path, names[i])




