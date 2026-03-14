import json
import re


# =========================
# CHUYỂN KÝ HIỆU TOÁN → LATEX
# =========================

def to_latex(text):

    if not text:
        return text

    # sqrt(x)
    text = re.sub(r"sqrt\((.*?)\)", r"\\sqrt{\1}", text)

    # sin cos tan
    text = re.sub(r"\bsin\b", r"\\sin", text)
    text = re.sub(r"\bcos\b", r"\\cos", text)
    text = re.sub(r"\btan\b", r"\\tan", text)

    # pi
    text = text.replace("pi","\\pi")

    # <= >=
    text = text.replace("<=","\\le")
    text = text.replace(">=","\\ge")

    # nhân
    text = text.replace("*","\\cdot ")

    # lũy thừa x^2
    text = re.sub(r"([a-zA-Z0-9])\^([0-9]+)", r"\1^{\2}", text)

    # đóng gói $
    return f"${text}$"


# =========================
# CHUYỂN DATASET
# =========================

def convert_dataset(input_file,output_file):

    with open(input_file,"r",encoding="utf-8") as f:
        data=json.load(f)

    for q in data:

        q["question"]=to_latex(q["question"])

        q["options"]=[to_latex(o) for o in q["options"]]

        q["answer"]=to_latex(q["answer"])

    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

    print("Đã tạo:",output_file)


# =========================

convert_dataset("dataset/math.json","math_latex.json")