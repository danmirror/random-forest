import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_text

# === STEP 1: BACA CSV ===
def load_csv(path):
    return pd.read_csv(path)

# === STEP 2: KONVERSI 1 TREE KE C++ ===
def convert_tree_to_if_else(tree_text, tree_index):
    lines = tree_text.strip().split('\n')
    result = [f'int predict_tree_{tree_index}(float temperature, int gsr, int bpm) {{']
    indent_stack = []

    for line in lines:
        if not line.strip():
            continue

        indent = line.count("|   ")
        content = line.lstrip("|- ")

        while indent_stack and indent <= indent_stack[-1]:
            result.append("    " * (indent_stack.pop() + 1) + "}")

        if "class:" in content:
            class_num = int(float(content.split("class: ")[-1]))
            result.append("    " * (indent + 1) + f'return {class_num};')
        elif "<=" in content or ">" in content:
            tokens = content.split()
            if len(tokens) >= 3:
                feature, op, value = tokens[0], tokens[1], tokens[2]
                result.append("    " * (indent + 1) + f'if ({feature} {op} {value}) {{')
                indent_stack.append(indent)

    while indent_stack:
        result.append("    " * (indent_stack.pop() + 1) + "}")
    result.append("}")
    return result

# === STEP 3: FUNGSI VOTING C++ ===
def create_voting_function(n_trees, label_map_reverse):
    code = [
        'String predictSensorCondition(float temperature, int gsr, int bpm) {',
        f'    int votes[{n_trees}];'
    ]
    code += [f'    votes[{i}] = predict_tree_{i}(temperature, gsr, bpm);' for i in range(n_trees)]
    code += [
        '    int count[10] = {0};',
        f'    for (int i = 0; i < {n_trees}; i++) count[votes[i]]++;',
        '    int max_idx = 0;',
        '    for (int i = 1; i < 10; i++) {',
        '        if (count[i] > count[max_idx]) max_idx = i;',
        '    }',
        '    switch (max_idx) {'
    ]
    for idx, label in label_map_reverse.items():
        code.append(f'        case {idx}: return "{label}";')
    code += [
        '        default: return "unknown";',
        '    }',
        '}'
    ]
    return code

# === STEP 4: LATIH MODEL & EXPORT ===
def generate_random_forest_code_from_csv(csv_path, n_trees=5, output_h="sensor_model.h"):
    df = load_csv(csv_path)
    X = df[["temperature", "gsr", "bpm"]]
    y = df["label"]

    label_map = {label: idx for idx, label in enumerate(y.unique())}
    label_map_reverse = {v: k for k, v in label_map.items()}
    y_encoded = y.map(label_map)

    model = RandomForestClassifier(n_estimators=n_trees, max_depth=5, random_state=42)
    model.fit(X, y_encoded)

    all_trees_code = []
    for i, estimator in enumerate(model.estimators_):
        tree_text = export_text(estimator, feature_names=X.columns.tolist())
        tree_code = convert_tree_to_if_else(tree_text, i)
        all_trees_code.extend(tree_code + [""])

    voting_code = create_voting_function(n_trees, label_map_reverse)

    final_code = [
        "#ifndef SENSOR_MODEL_H",
        "#define SENSOR_MODEL_H",
        "",
        f"// Random Forest with {n_trees} trees",
        ""
    ] + all_trees_code + voting_code + ["", "#endif"]

    with open(output_h, "w") as f:
        f.write("\n".join(final_code))

    print(f"✅ File '{output_h}' berhasil dibuat dengan {n_trees} pohon.")

# === CONTOH PAKAI ===
if __name__ == "__main__":
    generate_random_forest_code_from_csv("synthetic_sensor_data.csv", n_trees=5)
