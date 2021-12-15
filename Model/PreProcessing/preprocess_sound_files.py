import wave
import numpy as np
from os import listdir
import shutil, os, os.path
import subprocess
from os.path import isfile
import pandas as pd
from scipy.io.wavfile import write

# Sampling rate is 48kHz (originally)
sampling_rate = 48000


def read_sound_file(file):
    # Read file to get buffer
    ifile = wave.open(file)
    samples = ifile.getnframes()
    audio = ifile.readframes(samples)

    # Convert buffer to float32 using NumPy
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)

    # Normalise float32 array so that values are between -1.0 and +1.0
    max_int16 = 2 ** 15
    audio_normalised = audio_as_np_float32 / max_int16
    return audio_normalised


# Use old segmentation
def segment_cough(x, fs, cough_padding=0.2, min_cough_len=0.2, th_l_multiplier=0.1, th_h_multiplier=2):
    """Preprocess the data by segmenting each file into individual coughs using a hysteresis comparator on the signal power

    Inputs:
    *x (np.array): cough signal
    *fs (float): sampling frequency in Hz
    *cough_padding (float): number of seconds added to the beginning and end of each detected cough to make sure coughs are not cut short
    *min_cough_length (float): length of the minimum possible segment that can be considered a cough
    *th_l_multiplier (float): multiplier of the RMS energy used as a lower threshold of the hysteresis comparator
    *th_h_multiplier (float): multiplier of the RMS energy used as a high threshold of the hysteresis comparator

    Outputs:
    *coughSegments (np.array of np.arrays): a list of cough signal arrays corresponding to each cough
    cough_mask (np.array): an array of booleans that are True at the indices where a cough is in progress"""

    cough_mask = np.array([False] * len(x))

    # Define hysteresis thresholds
    rms = np.sqrt(np.mean(np.square(x)))
    seg_th_l = th_l_multiplier * rms
    seg_th_h = th_h_multiplier * rms

    # Segment coughs
    coughSegments = []
    padding = round(fs * cough_padding)
    min_cough_samples = round(fs * min_cough_len)
    cough_start = 0
    cough_end = 0
    cough_in_progress = False
    tolerance = round(0.01 * fs)
    below_th_counter = 0

    for i, sample in enumerate(x ** 2):
        if cough_in_progress:
            if sample < seg_th_l:
                below_th_counter += 1
                if below_th_counter > tolerance:
                    cough_end = i + padding if (i + padding < len(x)) else len(x) - 1
                    cough_in_progress = False
                    if (cough_end + 1 - cough_start - 2 * padding > min_cough_samples):
                        coughSegments.append(x[cough_start:cough_end + 1])
                        cough_mask[cough_start:cough_end + 1] = True
            elif i == (len(x) - 1):
                cough_end = i
                cough_in_progress = False
                if (cough_end + 1 - cough_start - 2 * padding > min_cough_samples):
                    coughSegments.append(x[cough_start:cough_end + 1])
            else:
                below_th_counter = 0
        else:
            if sample > seg_th_h:
                cough_start = i - padding if (i - padding >= 0) else 0
                cough_in_progress = True

    return coughSegments, cough_mask


def compute_SNR(x, fs):
    """Compute the Signal-to-Noise ratio of the audio signal x (np.array) with sampling frequency fs (float)"""
    segments, cough_mask = segment_cough(x, fs)
    RMS_signal = 0 if len(x[cough_mask]) == 0 else np.sqrt(np.mean(np.square(x[cough_mask])))
    RMS_noise = np.sqrt(np.mean(np.square(x[~cough_mask])))
    SNR = 0 if (RMS_signal == 0 or np.isnan(RMS_noise)) else 20 * np.log10(RMS_signal / RMS_noise)
    return SNR


def custom_segment(file, new_folder, cough_length):
    try:
        os.mkdir(new_folder)
    except:
        pass
    new_filenames = []
    length = []
    final = []
    max_int16 = 2 ** 15
    name = file.replace('.wav', '')
    np_file = read_sound_file(file)
    seg, seg_m = segment_cough(np_file, sampling_rate, cough_padding=1)
    for s in seg:
        segment, seg_m = segment_cough(s, sampling_rate, min_cough_len=0.01)
        for cough in segment:
            final.append(cough)

    for index, cough in enumerate(final):
        cough = pad_cough(cough, cough_length)
        cough = cough * max_int16  # undo normalized audio
        new_name = name + "_" + str(index)
        write(new_folder + '/' + new_name + '.wav', sampling_rate, cough.astype(np.int16))
        new_filenames.append(new_name)
        length.append(len(cough))

    return new_filenames, length


def pad_cough(np_cough, length):
    if len(np_cough) > length:
        np_cough = np_cough[:length]
    elif len(np_cough) < length:
        pad_len = length - len(np_cough)
        np_cough = np.pad(np_cough, (0, pad_len), 'constant', constant_values=(0, 0))
    return np_cough


def custom_segment_no_files(file, new_folder, cough_length):
    new_filenames = []
    np_coughs = []
    length = []
    final = []
    name = file.replace('.wav', '')
    np_file = read_sound_file(file)
    seg, seg_m = segment_cough(np_file, sampling_rate, cough_padding=1)
    for s in seg:
        segment, seg_m = segment_cough(s, sampling_rate, min_cough_len=0.01)
        for cough in segment:
            final.append(cough)

    for index, cough in enumerate(final):
        cough = pad_cough(cough, cough_length)
        new_name = name + "_" + str(index)
        new_filenames.append(new_name)
        np_coughs.append(cough)
        length.append(len(cough))

    return new_filenames, np_coughs, length


def convert_back_to_wave(np_cough, path, new_name):
    max_int16 = 2 ** 15
    np_cough = np_cough * max_int16
    write(path + '/' + new_name + '.wav', sampling_rate, np_cough.astype(np.int16))


def process_dataset(dataset, status):
    dataset.insert(1, 'fever_muscle_pain', '')
    dataset.insert(1, 'respiratory_condition', '')
    dataset.insert(1, 'gender', '')
    dataset.insert(1, 'age', '')
    dataset.insert(1, 'SNR', '')
    dataset.insert(1, 'status', '')

    data_main = pd.read_csv('data/metadata_compiled.csv')
    data_main = data_main[
        ['uuid', 'SNR', 'cough_detected', 'age', 'gender', 'respiratory_condition', 'fever_muscle_pain', 'status']]
    data_main = data_main[data_main['status'] == status]
    data_main = data_main[data_main['cough_detected'] > 0.15]

    for id in data_main['uuid']:
        dataset.loc[dataset['uuid'].str.contains(id), 'status'] = data_main[data_main['uuid'] == id]['status'].values[0]
        dataset.loc[dataset['uuid'].str.contains(id), 'SNR'] = data_main[data_main['uuid'] == id]['SNR'].values[0]
        dataset.loc[dataset['uuid'].str.contains(id), 'age'] = data_main[data_main['uuid'] == id]['age'].values[0]
        dataset.loc[dataset['uuid'].str.contains(id), 'gender'] = data_main[data_main['uuid'] == id]['gender'].values[0]
        dataset.loc[dataset['uuid'].str.contains(id), 'respiratory_condition'] = \
            data_main[data_main['uuid'] == id]['respiratory_condition'].values[0]
        dataset.loc[dataset['uuid'].str.contains(id), 'fever_muscle_pain'] = \
            data_main[data_main['uuid'] == id]['fever_muscle_pain'].values[0]

    return dataset


def segment_to_dataframe(path):
    os.chdir(path)
    files = listdir()
    all_names = []
    all_coughs = []
    all_length = []
    for index, file in enumerate(files):
        print(index, "  file: ", file)
        if isfile(file):
            new_names, coughs, lengths = custom_segment_no_files(file, 'segmented', 30000)
            all_names = all_names + new_names
            all_length = all_length + lengths
            all_coughs = all_coughs + coughs

    dataset = pd.DataFrame({'uuid': all_names, 'cough': all_coughs}, columns=['uuid', 'cough'])
    os.chdir('../../../')
    print("done")
    return dataset


def final_processing(path, status):
    data = segment_to_dataframe(path)
    all_coughs = data['cough']
    all_names = data['uuid']
    # ====================
    # Convert to wav
    # comment this out if segmented wav files not needed
    # ======================
    seg_path = path + '/segmented'
    try:
        os.mkdir(seg_path)
    except:
        pass
    for i, c in enumerate(all_coughs):
        convert_back_to_wave(c, seg_path, all_names[i])
    # ============
    # Add columns to dataset
    # ===============
    dataset = process_dataset(data, status)
    return dataset


# ==============================================
# Start
# ==============================================

# 'COVID-19'

# print("start")
# path = 'data/covid/wav'
# df = final_processing(path, 'COVID-19')  # requires wav files in path in a "/wav" folder
# df.to_pickle('output_covid.pkl')

# print("start")
# path = 'data/symptomatic/wav'
# df = final_processing(path, 'symptomatic')  # requires wav files in path in a "/wav" folder
# df.to_pickle('output_symptomatic.pkl')
# print("all done")

print("start")
path = 'data/healthy/wav'
df = final_processing(path, 'healthy')  # requires wav files in path in a "/wav" folder
df.to_pickle('output_healthy.pkl')
print("all done")



