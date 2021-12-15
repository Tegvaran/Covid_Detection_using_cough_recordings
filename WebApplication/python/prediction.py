from tensorflow import keras
import json
import os
import numpy as np
import sys 

DATASET_PATH = "file/" + sys.argv[1]
DATA_PATH = "file/" + sys.argv[1] + '/data.json'
# DATASET_PATH = "file/" + '1638153856406'
# DATA_PATH = "file/" + '1638153856406'+ "/data.json"

MAPPING = {
    0: "COVID-19",
    1: "Healthy"
}

MODEL_PATH = 'over_sampling_dirty'
model = keras.models.load_model(MODEL_PATH)

with open(DATA_PATH, "r") as fp:
    data = json.load(fp)

X = np.array(data["mfcc"])
pred = model.predict(X)
prediction = []

for p in pred:
    p_list = p.tolist()
    prediction.append(p_list[0])
print(prediction, end="")

