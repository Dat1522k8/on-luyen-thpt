import json
import re

input_file = "dataset/math.json"
output_file = "dataset_fixed.json"

def fix_question(text):

    text = text.strip()

    # bỏ $ bao quanh cả câu
    if text.startswith("$") and text.endswith("$"):
        text = text[1:-1]

    # thêm $ quanh biểu thức có ^
    text = re.sub(r'(x\^\{?\d+\}?)', r'$\1$', text)

    return text


with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for q in data:
    q["question"] = fix_question(q["question"])

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✔ Dataset đã sửa xong")