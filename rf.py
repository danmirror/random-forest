from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_text
import pandas as pd

# 1. Data training (buatan contoh)
data = pd.DataFrame({
    'suhu':       [30, 25, 22, 35, 27, 29, 21, 33],
    'kelembaban': [40, 60, 70, 30, 65, 55, 85, 35],
    'cahaya':     [900, 600, 400, 1000, 500, 450, 200, 800],
    'label':      ['PANAS', 'NORMAL', 'LEMBAB', 'PANAS', 'NORMAL', 'NORMAL', 'LEMBAB', 'PANAS']
})

# 2. Label encode
label_map = {'PANAS': 0, 'NORMAL': 1, 'LEMBAB': 2}
data['label'] = data['label'].map(label_map)

# 3. Model training
X = data[['suhu', 'kelembaban', 'cahaya']]
y = data['label']

model = RandomForestClassifier(n_estimators=1, max_depth=4, random_state=42)
model.fit(X, y)

# 4. Tampilkan pohon keputusan
rules = export_text(model.estimators_[0], feature_names=['suhu', 'kelembaban', 'cahaya'])
print(rules)

# 5. Cek importance fitur
importances = model.feature_importances_
for feat, imp in zip(['suhu', 'kelembaban', 'cahaya'], importances):
    print(f"{feat}: {imp:.3f}")
