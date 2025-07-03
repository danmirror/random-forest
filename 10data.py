import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_text

def convert_tree_to_if_else(tree_text, tree_index):
    lines = tree_text.strip().split('\n')
    result = [f'int predict_tree_{tree_index}(float temperature, int gsr, int bpm) {{']
    indent_stack = []

    prev_indent = -1
    for i, line in enumerate(lines):
        if not line.strip():
            continue

        indent = line.count("|   ")
        content = line.lstrip("|- ")

        # Tutup blok-blok sebelumnya jika indent turun
        while indent_stack and indent <= indent_stack[-1]:
            result.append("    " * (indent_stack.pop() + 1) + "}")

        if "class:" in content:
            try:
                class_num = int(float(content.split("class: ")[-1]))
                result.append("    " * (indent + 1) + f'return {class_num};')
            except ValueError:
                continue
        elif "<=" in content or ">" in content:
            tokens = content.split()
            if len(tokens) >= 3:
                feature, op, value = tokens[0], tokens[1], tokens[2]
                result.append("    " * (indent + 1) + f'if ({feature} {op} {value}) {{')
                indent_stack.append(indent)

        prev_indent = indent

    # Tutup semua blok yang tersisa
    while indent_stack:
        result.append("    " * (indent_stack.pop() + 1) + "}")

    result.append("}")
    return result


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


# Fungsi utama
def generate_random_forest_code(df, n_trees=5, output_file="sensor_model.h"):
    # Fitur dan label
    X = df[["temperature", "gsr", "bpm"]]
    y = df["label"]
    label_map = {label: idx for idx, label in enumerate(y.unique())}
    label_map_reverse = {v: k for k, v in label_map.items()}
    y_encoded = y.map(label_map)

    # Latih model
    model = RandomForestClassifier(n_estimators=n_trees, max_depth=5, random_state=42)
    model.fit(X, y_encoded)

    # Konversi semua pohon
    all_trees_code = []
    for i, estimator in enumerate(model.estimators_):
        tree_text = export_text(estimator, feature_names=X.columns.tolist())
        tree_code = convert_tree_to_if_else(tree_text, i)
        all_trees_code.extend(tree_code + [""])

    # Tambah fungsi voting
    voting_code = create_voting_function(n_trees, label_map_reverse)

    # Gabungkan semua bagian
    final_code = [
        "#ifndef SENSOR_MODEL_H",
        "#define SENSOR_MODEL_H",
        "",
        f"// Random Forest with {n_trees} trees",
        ""
    ] + all_trees_code + voting_code + ["", "#endif"]

    # Simpan ke file
    with open(output_file, "w") as f:
        f.write("\n".join(final_code))

    print(f"✅ File '{output_file}' berhasil dibuat dengan {n_trees} pohon.")


# Data dari gambar
data = [
    [3.11, 32.32, 77, "Calm"],
    [5.67, 34.18, 71, "Anxious"],
    [3.81, 37.13, 67, "Relax"],
    [4.85, 35.44, 75, "Calm"],
    [3.48, 35.67, 76, "Calm"],
    [3.14, 32.45, 70, "Calm"],
    [4.79, 35.53, 69, "Calm"],
    [4.42, 37.25, 85, "Stress"],
    [3.31, 32.58, 69, "Calm"],
    [3.09, 35.44, 85, "Calm"]
]

df = pd.DataFrame(data, columns=["gsr", "temperature", "bpm", "label"])

# Fungsi convert_tree_to_if_else & generate_random_forest_code → pakai versi perbaikan terakhir yang sudah kita bahas

# Lanjutkan dengan:
generate_random_forest_code(df, n_trees=3, output_file="sensor_model.h")


