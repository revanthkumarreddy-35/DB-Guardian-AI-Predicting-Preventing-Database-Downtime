import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

SEQ_LEN = 50

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATA_DIR, "mysql_metrics.csv"))
df = df.dropna()

features = df.iloc[:, 1:].values
scaled = MinMaxScaler().fit_transform(features)

X = []
for i in range(len(scaled) - SEQ_LEN):
    X.append(scaled[i:i + SEQ_LEN])

X = np.array(X)
np.save(os.path.join(DATA_DIR, "X.npy"), X)

print("Preprocessing completed.")
