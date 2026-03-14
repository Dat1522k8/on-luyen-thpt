import json
import random

questions=[]

# =========================
# câu hỏi định luật Newton
# =========================

for i in range(40):

    m=random.randint(1,10)
    a=random.randint(1,10)

    F=m*a

    q={
        "question":f"Một vật có khối lượng {m} kg chuyển động với gia tốc {a} m/s^2. Lực tác dụng lên vật là bao nhiêu?",
        "options":[
            f"{F} N",
            f"{F+5} N",
            f"{F-3} N",
            f"{F+10} N"
        ],
        "answer":f"{F} N",
        "concept":"luc"
    }

    random.shuffle(q["options"])
    questions.append(q)

# =========================
# câu hỏi vận tốc
# =========================

for i in range(40):

    s=random.randint(20,200)
    t=random.randint(2,10)

    v=round(s/t,2)

    q={
        "question":f"Một vật đi được quãng đường {s} m trong {t} s. Vận tốc của vật là bao nhiêu?",
        "options":[
            f"{v} m/s",
            f"{v+2} m/s",
            f"{v+5} m/s",
            f"{v-1} m/s"
        ],
        "answer":f"{v} m/s",
        "concept":"van_toc"
    }

    random.shuffle(q["options"])
    questions.append(q)

# =========================
# câu hỏi công
# =========================

for i in range(40):

    F=random.randint(10,100)
    s=random.randint(2,10)

    A=F*s

    q={
        "question":f"Một lực {F} N tác dụng làm vật dịch chuyển {s} m. Công thực hiện là bao nhiêu?",
        "options":[
            f"{A} J",
            f"{A+20} J",
            f"{A-10} J",
            f"{A+50} J"
        ],
        "answer":f"{A} J",
        "concept":"cong"
    }

    random.shuffle(q["options"])
    questions.append(q)

# =========================
# câu hỏi điện
# =========================

for i in range(40):

    I=random.randint(1,10)
    R=random.randint(1,20)

    U=I*R

    q={
        "question":f"Một mạch điện có cường độ dòng điện {I} A và điện trở {R} Ω. Hiệu điện thế là bao nhiêu?",
        "options":[
            f"{U} V",
            f"{U+5} V",
            f"{U+10} V",
            f"{U-2} V"
        ],
        "answer":f"{U} V",
        "concept":"dien_ap"
    }

    random.shuffle(q["options"])
    questions.append(q)

# ======================
# TỪ TRƯỜNG
# ======================

for i in range(40):

    B=round(random.uniform(0.1,1),2)
    I=random.randint(1,10)
    l=random.randint(1,5)

    F=round(B*I*l,2)

    q={
        "question":f"Một dây dẫn dài {l} m đặt trong từ trường có cảm ứng từ {B} T, dòng điện {I} A. Lực từ tác dụng lên dây là bao nhiêu?",
        "options":[
            f"{F} N",
            f"{F+0.5} N",
            f"{F+1} N",
            f"{F-0.2} N"
        ],
        "answer":f"{F} N",
        "concept":"tu_truong"
    }

    random.shuffle(q["options"])
    questions.append(q)

# ======================
# KHÍ LÝ TƯỞNG
# ======================

for i in range(40):

    n=random.randint(1,5)
    R=8.31
    T=random.randint(300,500)

    pV=round(n*R*T,2)

    q={
        "question":f"Một lượng khí có số mol {n}, nhiệt độ {T} K. Theo phương trình khí lý tưởng pV = nRT. Giá trị pV bằng bao nhiêu?",
        "options":[
            f"{pV}",
            f"{pV+100}",
            f"{pV+200}",
            f"{pV-50}"
        ],
        "answer":f"{pV}",
        "concept":"khi_ly_tuong"
    }

    random.shuffle(q["options"])
    questions.append(q)

# ======================
# NHIỆT HỌC
# ======================

for i in range(40):

    m=random.randint(1,5)
    c=4200
    dt=random.randint(5,20)

    Q=m*c*dt

    q={
        "question":f"Một vật có khối lượng {m} kg, nhiệt dung riêng 4200 J/kg.K, tăng nhiệt độ {dt}°C. Nhiệt lượng thu vào là bao nhiêu?",
        "options":[
            f"{Q} J",
            f"{Q+1000} J",
            f"{Q+2000} J",
            f"{Q-500} J"
        ],
        "answer":f"{Q} J",
        "concept":"nhiet_hoc"
    }

    random.shuffle(q["options"])
    questions.append(q)

# ======================
# HẠT NHÂN
# ======================

for i in range(40):

    A=random.randint(10,50)
    Z=random.randint(5,25)

    N=A-Z

    q={
        "question":f"Hạt nhân có số khối {A} và số proton {Z}. Số neutron là bao nhiêu?",
        "options":[
            f"{N}",
            f"{N+1}",
            f"{N+2}",
            f"{N-1}"
        ],
        "answer":f"{N}",
        "concept":"hat_nhan"
    }

    random.shuffle(q["options"])
    questions.append(q)

# =========================
# ghi file json
# =========================

with open("dataset/physics.json","w",encoding="utf-8") as f:
    json.dump(questions,f,ensure_ascii=False,indent=4)

print("Đã tạo",len(questions),"câu hỏi vật lý")