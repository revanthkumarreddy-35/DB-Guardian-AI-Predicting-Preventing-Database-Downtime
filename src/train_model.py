import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Input, RepeatVector, TimeDistributed, Dense

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

X = np.load(os.path.join(DATA_DIR, "X.npy"))

inputs = Input(shape=(X.shape[1], X.shape[2]))
encoded = LSTM(64, activation="relu")(inputs)
encoded = RepeatVector(X.shape[1])(encoded)
decoded = LSTM(64, activation="relu", return_sequences=True)(encoded)
decoded = TimeDistributed(Dense(X.shape[2]))(decoded)

model = Model(inputs, decoded)
model.compile(optimizer="adam", loss="mse")

history = model.fit(X, X, epochs=20, batch_size=32, validation_split=0.1)

model.save(os.path.join(MODELS_DIR, "lstm_autoencoder.h5"))

plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.legend()
plt.show()
