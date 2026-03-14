import json
import random
import os

file_path="dataset/math.json"

questions=[]

# ===== ĐẠO HÀM =====

for i in range(400):

    n=random.randint(2,8)

    question=f"Đạo hàm của x^{n} là gì?"

    correct=f"{n}x^{n-1}"

    options=[
        correct,
        f"{n-1}x^{n}",
        f"x^{n}",
        f"{n}x^{n}"
    ]

    random.shuffle(options)

    questions.append({

    "question":question,

    "options":options,

    "answer":correct,

    "concept":"dao_ham"

    })


# ===== NGUYÊN HÀM =====

for i in range(400):

    n=random.randint(1,6)

    question=f"Nguyên hàm của x^{n} là gì?"

    correct=f"x^{n+1}/{n+1}+C"

    options=[
        correct,
        f"{n}x^{n}+C",
        f"x^{n}+C",
        f"x^{n+2}+C"
    ]

    random.shuffle(options)

    questions.append({

    "question":question,

    "options":options,

    "answer":correct,

    "concept":"nguyen_ham"

    })


# ===== LOGARIT =====

for i in range(400):

    n=random.randint(1,5)

    value=10**n

    question=f"log10({value}) bằng bao nhiêu?"

    correct=str(n)

    options=[
        correct,
        str(n+1),
        str(max(0,n-1)),
        str(n+2)
    ]

    random.shuffle(options)

    questions.append({

    "question":question,

    "options":options,

    "answer":correct,

    "concept":"logarit"

    })


# ===== CẤP SỐ CỘNG =====

for i in range(400):

    a=random.randint(1,10)

    d=random.randint(1,6)

    n=random.randint(3,10)

    result=a+(n-1)*d

    question=f"Cấp số cộng có a1={a}, d={d}. Tính a{n}"

    options=[
        str(result),
        str(result+1),
        str(result-1),
        str(result+2)
    ]

    random.shuffle(options)

    questions.append({

    "question":question,

    "options":options,

    "answer":str(result),

    "concept":"cap_so_cong"

    })


# ===== CẤP SỐ NHÂN =====

for i in range(400):

    a=random.randint(1,5)

    q=random.randint(2,4)

    n=random.randint(3,8)

    result=a*(q**(n-1))

    options=[
        str(result),
        str(result+2),
        str(result-2),
        str(result+4)
    ]

    random.shuffle(options)

    questions.append({

    "question":f"Cấp số nhân có a1={a}, q={q}. Tính a{n}",

    "options":options,

    "answer":str(result),

    "concept":"cap_so_nhan"

    })

# ===== XÁC SUẤT =====

for i in range(400):

    loai=random.randint(1,4)

    # ===== XÁC SUẤT ĐƠN =====
    if loai==1:

        n=random.randint(4,12)

        k=random.randint(1,n)

        question=f"Một hộp có {n} viên bi, trong đó có {k} viên đỏ. Lấy ngẫu nhiên 1 viên. Xác suất lấy được bi đỏ là?"

        correct=f"{k}/{n}"

        options=[
            correct,
            f"{k+1}/{n}",
            f"{k}/{n+1}",
            f"{k+2}/{n}"
        ]

        concept="xac_suat"


    # ===== XÁC SUẤT CÓ ĐIỀU KIỆN =====
    elif loai==2:

        question="Nếu P(A)=0.5, P(B)=0.4 và P(A∩B)=0.2 thì P(A|B) bằng?"

        correct="0.5"

        options=["0.5","0.4","0.2","0.8"]

        concept="xac_suat_co_dieu_kien"


    # ===== XÁC SUẤT TOÀN PHẦN =====
    elif loai==3:

        question="Nếu P(A|B)=0.6, P(B)=0.5, P(A|B')=0.2 thì P(A) bằng?"

        correct="0.4"

        options=["0.4","0.3","0.5","0.6"]

        concept="xac_suat_toan_phan"


    # ===== BAYES =====
    else:

        question="Theo định lý Bayes: P(B|A)=?"

        correct="P(A|B)P(B)/P(A)"

        options=[
            correct,
            "P(A)P(B)",
            "P(A|B)/P(B)",
            "P(B)/P(A)"
        ]

        concept="bayes"


    random.shuffle(options)

    questions.append({

        "question":question,

        "options":options,

        "answer":correct,

        "concept":concept

    })

# ===== ĐỌC FILE CŨ =====

if os.path.exists(file_path):

    with open(file_path,"r",encoding="utf-8") as f:
        old_data=json.load(f)

else:
    old_data=[]


# ===== GỘP DATASET =====

old_data.extend(questions)


# ===== GHI FILE =====

with open(file_path,"w",encoding="utf-8") as f:

    json.dump(old_data,f,ensure_ascii=False,indent=4)


print("Đã thêm",len(questions),"câu hỏi")

print("Tổng số câu:",len(old_data))