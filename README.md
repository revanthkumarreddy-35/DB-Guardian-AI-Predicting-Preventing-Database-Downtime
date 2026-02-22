# DB Guardian AI

A deep learning system to predict MySQL database downtime using LSTM Autoencoders.

## Steps to Run

1. Install dependencies  
   pip install -r requirements.txt

2. Run data collection  
   python src/data_collection.py

3. Train model  
   python src/preprocess.py  
   python src/train_model.py

4. Detect anomalies  
   python src/anomaly_detection.py
