import json
import random
import os

# ==========================================
# 1. CÁC HÀM SINH CÂU HỎI THEO CHỦ ĐỀ
# ==========================================

def generate_physics_dataset(num_questions=50):
    dataset = []
    for i in range(num_questions):
        level = random.choice(["Trung bình", "Khó"])
        concept = random.choice(["tu_truong", "hat_nhan", "khi_ly_tuong", "nhiet_dong_luc_hoc"])
        
        if concept == "khi_ly_tuong":
            p = random.randint(1, 5)
            v = random.randint(10, 20)
            if level == "Trung bình":
                q = f"Một khối khí giãn nở đẳng áp ở áp suất ${p} \\cdot 10^5 Pa$. Thể tích tăng từ ${v}l$ lên ${v+10}l$. Công khối khí thực hiện là?"
                ans = f"${p * 10^3} J$"
            else:
                q = f"Khối khí lý tưởng thực hiện quá trình đoạn nhiệt. Nếu thể tích giảm nửa thì áp suất thay đổi thế nào? (Biết $\\gamma = 1.4$)"
                ans = "Tăng $2.64$ lần"
        
        elif concept == "hat_nhan":
            T = random.choice([2, 5, 8, 138])
            time = T * random.randint(2, 4)
            if level == "Trung bình":
                q = f"Chu kỳ bán rã của một chất là ${T}$ ngày. Sau ${time}$ ngày, lượng chất còn lại bao nhiêu phần trăm?"
                ans = f"${round((1/(2**(time/T)))*100, 2)}\\%$"
            else:
                q = f"Tính năng lượng liên kết riêng của hạt nhân $^{{210}}_{{84}}Po$ biết khối lượng proton là $1.00728u$ và neutron là $1.00866u$."
                ans = "7.4 MeV/nucleon"
        else:
            q = f"Đặc điểm nào sau đây là của đường sức từ trong lòng một nam châm chữ U?"
            ans = "Là các đường thẳng song song cách đều nhau"
        
        options = [ans, "Đáp án sai A", "Đáp án sai B", "Đáp án sai C"]
        random.shuffle(options)
        dataset.append({"level": level, "question": q, "options": options, "answer": ans, "concept": concept, "theory": "Lý thuyết tổng hợp."})
    return dataset

def generate_physics_dataset_pro(num_questions=50):
    dataset = []
    for i in range(num_questions):
        level = random.choice(["Khó", "Nâng cao (VDC)"])
        concept = random.choice(["tu_truong", "hat_nhan", "khi_ly_tuong", "nhiet_dong_luc_hoc"])
        
        if concept == "nhiet_dong_luc_hoc":
            if level == "Nâng cao (VDC)":
                q = "Một máy nhiệt lý tưởng hoạt động theo chu trình Carnot giữa $T_1 = 600K$ và $T_2 = 300K$. Máy nhận $Q_1 = 1200J$. Tính công thực tế nếu hao phí thêm 10%."
                ans = "$540J$"
                theory = "A' = 0.9 * Q1 * (1 - T2/T1)"
            else:
                q = "Nội năng của khí lý tưởng đơn nguyên tử biến thiên thế nào trong quá trình đẳng áp?"
                ans = "Tăng theo nhiệt độ"
                theory = "U = 3/2 nRT"
        elif concept == "hat_nhan":
            q = "Hạt $\\alpha$ bắn vào $^{14}N$ đứng yên gây phản ứng thu nhiệt $1.21 MeV$. Động năng tối thiểu của hạt $\\alpha$ là:"
            ans = "$1.56 MeV$"
            theory = "Kmin = |Q|*(m1+m2)/m2"
        else:
            q = f"Câu hỏi chuyên sâu về {concept} mức độ {level} dành cho học sinh giỏi."
            ans = "Đáp án phân tích đúng"

        options = [ans, "Phương án nhiễu 1", "Phương án nhiễu 2", "Phương án nhiễu 3"]
        random.shuffle(options)
        dataset.append({"level": level, "question": q, "options": options, "answer": ans, "concept": concept, "theory": "Phân tích VDC."})
    return dataset

# ==========================================
# 2. THỰC THI CHÍNH (MAIN) - KHÔI PHỤC TOÀN BỘ VÒNG LẶP CỦA BẠN
# ==========================================
if __name__ == "__main__":
    file_path = "dataset/physics.json"
    all_questions = []

    # A. Đọc dữ liệu cũ để ghi tiếp
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            all_questions = json.load(f)

    # B. Thêm các câu hỏi từ hàm sinh
    all_questions.extend(generate_physics_dataset(50))
    all_questions.extend(generate_physics_dataset_pro(50))

    # C. Khôi phục các vòng lặp chi tiết của bạn
    # --- TỪ TRƯỜNG ---
    for _ in range(25):
        I, L, B = random.randint(2, 5), random.randint(1, 2), round(random.uniform(0.1, 0.5), 2)
        F = round(B * I * L, 2)
        all_questions.append({
            "level": "Trung bình",
            "question": f"Một dây dẫn thẳng dài {L}m đặt vuông góc với từ trường đều $B = {B}T$. Dòng điện qua dây là {I}A. Lực từ là:",
            "options": [f"{F} N", f"{F*2} N", "0 N", f"{F/2} N"],
            "answer": f"{F} N", "concept": "tu_truong", "theory": "F = BIl.sin(90)"
        })

    # --- HẠT NHÂN ---
    for _ in range(25):
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Cho phản ứng nhiệt hạch: $^2_1D + ^3_1T \\rightarrow ^4_2He + ^1_0n$. Năng lượng tỏa ra là:",
            "options": ["17.6 MeV", "15.3 MeV", "20.1 MeV", "12.4 MeV"],
            "answer": "17.6 MeV", "concept": "hat_nhan", "theory": "Q = (lk_sau) - (lk_truoc)"
        })

    # --- KHÍ LÝ TƯỞNG ---
    for _ in range(20):
        V1, T1, T2 = 2, 300, 600
        V2 = V1 * (T2/T1)
        all_questions.append({
            "level": "Trung bình",
            "question": f"Khối khí thể tích {V1}l ở {T1}K. Nung nóng đẳng áp lên {T2}K thì thể tích là:",
            "options": [f"{V2} lít", "1 lít", "4 lít", "3 lít"],
            "answer": f"{V2} lít", "concept": "khi_ly_tuong", "theory": "V/T = const"
        })

    # --- ĐỊNH LUẬT NEWTON ---
    for _ in range(20):
        m, a = random.randint(1, 10), random.randint(1, 10)
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Vật khối lượng {m}kg, gia tốc {a}m/s2. Lực tác dụng là:",
            "options": [f"{m*a} N", f"{m+a} N", f"{m-a} N", "0 N"],
            "answer": f"{m*a} N", "concept": "luc", "theory": "F = ma"
        })

    # D. Lưu lại file
    os.makedirs("dataset", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)

    print(f"✅ Đã xong! Tổng cộng file đang có {len(all_questions)} câu hỏi.")