import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Labeling dengan suhu, gsr, dan bpm
def label_sample(temperature, gsr, bpm):
    if temperature > 38.0 and bpm > 95:
        return "stressed"
    elif temperature < 36.0 and bpm < 70 and gsr < 400:
        return "relaxed"
    elif 36.0 <= temperature <= 37.5 and 70 <= bpm <= 90 and 400 <= gsr <= 600:
        return "normal"
    else:
        return "stressed"

# Generate data dummy
def generate_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        temperature = round(random.uniform(32.0, 39.0), 1)
        gsr = random.randint(300, 700)
        bpm = random.randint(60, 120)
        label = label_sample(temperature, gsr, bpm)
        data.append([temperature, gsr, bpm, label])
    return pd.DataFrame(data, columns=["temperature", "gsr", "bpm", "label"])

# Generate & simpan data
df = generate_data(100)
df.to_csv("dummy_sensor_data.csv", index=False)
print("Contoh data:")
print(df.head())

# Pisahkan fitur dan label
X = df[["temperature", "gsr", "bpm"]]
y = df["label"]

# Split training dan testing 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Latih Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediksi & evaluasi
y_pred = model.predict(X_test)
print("\nAkurasi:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Coba prediksi satu data baru
new_sample = pd.DataFrame([[37.8, 580, 100]], columns=["temperature", "gsr", "bpm"])
prediction = model.predict(new_sample)
print("\nPrediksi data baru:")
print(new_sample)
print("Hasil prediksi:", prediction[0])
