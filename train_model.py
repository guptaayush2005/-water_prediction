import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

import joblib

# =========================
# LOAD DATASET
# =========================

file = pd.read_csv("dataset.csv")

# =========================
# SCALING
# =========================

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(file)

# =========================
# CREATE SEQUENCES
# =========================

X = []
y = []

sequence_length = 7

for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i, 0])
    y.append(scaled_data[i, 0])

X = np.array(X)
y = np.array(y)

# Reshape for LSTM
X = X.reshape((X.shape[0], X.shape[1], 1))

# =========================
# BUILD MODEL
# =========================

model = Sequential()

model.add(
    LSTM(
        64,
        activation='relu',
        input_shape=(X.shape[1], 1)
    )
)

model.add(Dense(32, activation='relu'))
model.add(Dense(1))

# =========================
# COMPILE MODEL
# =========================

model.compile(
    optimizer='adam',
    loss='mse'
)

# =========================
# TRAIN MODEL
# =========================

model.fit(
    X,
    y,
    epochs=100,
    batch_size=8
)

# =========================
# SAVE MODEL
# =========================

model.save("water_model.h5")

joblib.dump(scaler, "scaler.pkl")

print("✅ Model Trained Successfully")
