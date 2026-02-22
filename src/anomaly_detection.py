import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

SEQ_LEN = 50

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

model = tf.keras.models.load_model(
    os.path.join(MODELS_DIR, "lstm_autoencoder.h5"),
    compile=False
)

df = pd.read_csv(os.path.join(DATA_DIR, "mysql_metrics.csv"))
features = df.iloc[:, 1:].values
scaled = MinMaxScaler().fit_transform(features)

X = []
for i in range(len(scaled) - SEQ_LEN):
    X.append(scaled[i:i + SEQ_LEN])

X = np.array(X)

recon = model.predict(X, verbose=0)
mse = np.mean((X - recon) ** 2, axis=(1, 2))
threshold = np.percentile(mse, 95)

print("Anomaly threshold:", threshold)
print("Latest anomaly score:", mse[-1])

if mse[-1] > threshold:
    print("🚨 ALERT: Potential database downtime detected!")
else:
    print("✅ Database operating normally.")
