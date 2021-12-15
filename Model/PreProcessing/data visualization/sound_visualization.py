import scipy.io.wavfile
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
# read ECG data from the WAV file

SHOW_PEAKS = False
length = 7500
sampleRate, data = scipy.io.wavfile.read('healthy_cleaned.wav')
times = np.arange(len(data))/sampleRate

# apply a 3-pole lowpass filter at 0.1x Nyquist frequency
# b, a = scipy.signal.butter(3, 0.1, 'highpass')
# filtered = scipy.signal.filtfilt(b, a, data)


# plot the original data next to the filtered data

# plt.figure(figsize=(10, 4))
#
# plt.subplot(121)
# plt.plot(times, data)
# plt.title("ECG Signal with Noise")
# plt.margins(0, .05)
#
# plt.subplot(122)
# plt.plot(times, filtered)
# plt.title("Filtered ECG Signal")
# plt.margins(0, .05)
#
# plt.tight_layout()
# plt.show()
#
# # scipy.io.wavfile.write('output.wav', 12000, data.astype(np.int16))
# scipy.io.wavfile.write('output.wav', 12000, filtered.astype(np.int16))




# peaks, properties = find_peaks(data, prominence=(20000, None), distance=2000)
# max_idx = properties["prominences"].argmax()


# low_peaks, properties = find_peaks(data, prominence=(None, 1))
# start, end = low_peaks[0], low_peaks[-1]


# =================
if SHOW_PEAKS:
    max = 1
    low_peaks = []
    while len(low_peaks) < 2 or (low_peaks[-1] - low_peaks[0]) < 2000:
        print(len(low_peaks))
        low_peaks, properties = find_peaks(data, prominence=(None, max))
        max = max + 1

    start, end = low_peaks[0], low_peaks[-1]

    # ======================

    # plt.plot(data)
    # plt.plot(low_peaks, data[low_peaks], "x")
    # plt.show()

    for i, p in enumerate(low_peaks):
        if (p - start) < 2000:
            start = p
        else:
            end = low_peaks[i]
            break


plt.figure(figsize=(7, 5))
plt.plot(times, data)
plt.suptitle('Healthy')
plt.title('Segmented and Cleaned')
plt.xlabel('time(s)')
plt.ylabel('amplitude')
if SHOW_PEAKS:
    plt.plot([start/sampleRate, end/sampleRate], data[[start, end]], "x", markersize=16, mew=5)
plt.show()

# trimmed = data[start:end]
# padded = np.pad(trimmed, (0, length - len(trimmed)), 'constant')