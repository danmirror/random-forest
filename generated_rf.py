import pandas as pd
import random

def generate_synthetic_sensor_data(n_samples=100, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n_samples):
        # Pilih label berdasarkan probabilitas
        label = random.choices(["Calm", "Stress", "Anxious", "Relax"], weights=[0.4, 0.2, 0.2, 0.2])[0]
        
        # Range masing-masing label
        if label == "Calm":
            temp = round(random.uniform(35.0, 36.5), 2)
            gsr = round(random.uniform(3.0, 4.5), 2)
            bpm = random.randint(65, 75)
        elif label == "Stress":
            temp = round(random.uniform(36.5, 38.0), 2)
            gsr = round(random.uniform(4.5, 6.5), 2)
            bpm = random.randint(80, 95)
        elif label == "Anxious":
            temp = round(random.uniform(34.5, 36.0), 2)
            gsr = round(random.uniform(5.0, 6.5), 2)
            bpm = random.randint(70, 85)
        elif label == "Relax":
            temp = round(random.uniform(36.0, 37.5), 2)
            gsr = round(random.uniform(3.0, 4.5), 2)
            bpm = random.randint(60, 70)

        data.append([gsr, temp, bpm, label])

    df = pd.DataFrame(data, columns=["gsr", "temperature", "bpm", "label"])
    return df

# Contoh penggunaan:
df = generate_synthetic_sensor_data(n_samples=100, seed=42)
df.to_csv("synthetic_sensor_data.csv", index=False)