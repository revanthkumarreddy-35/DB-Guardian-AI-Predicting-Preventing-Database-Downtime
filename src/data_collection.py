import mysql.connector
import psutil
import time
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "mysql_metrics.csv")

# Delete old data for fresh run
if os.path.exists(file_path):
    os.remove(file_path)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",   # 👈 teammates change this
    "database": "mysql"
}

with open(file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "connections", "running_threads", "cpu", "memory", "disk"])

    while True:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SHOW GLOBAL STATUS LIKE 'Threads_connected'")
            connections = int(cursor.fetchone()[1])

            cursor.execute("SHOW GLOBAL STATUS LIKE 'Threads_running'")
            running = int(cursor.fetchone()[1])

            conn.close()

            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            writer.writerow([time.time(), connections, running, cpu, memory, disk])
            f.flush()

            print("Metrics collected...")
            time.sleep(10)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)
