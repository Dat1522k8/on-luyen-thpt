import json
import random
import os

# ==========================================
# 1. HÀM SINH CÂU HỎI VẬT LÝ CƠ BẢN/TRUNG BÌNH
# ==========================================
def generate_physics_dataset(num_questions=500):
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
            q = f"Câu hỏi {concept} mức độ {level} mẫu số {i}"
            ans = "Đáp án đúng mẫu"

        options = [ans, "Đáp án nhiễu A", "Đáp án nhiễu B", "Đáp án nhiễu C"]
        random.shuffle(options)

        dataset.append({
            "level": level,
            "question": q,
            "options": options,
            "answer": ans,
            "concept": concept,
            "theory": f"Lý thuyết cơ bản về {concept}."
        })

    return dataset

# ==========================================
# 2. HÀM SINH CÂU HỎI VẬT LÝ NÂNG CAO (VDC)
# ==========================================
import random

def generate_physics_dataset_pro(num_questions=500):
    dataset = []
    for i in range(num_questions):
        level = random.choice(["Khó", "Nâng cao (VDC)"])
        concept = random.choice(["tu_truong", "hat_nhan", "khi_ly_tuong", "nhiet_dong_luc_hoc"])
        
        q = f"Câu hỏi nâng cao về {concept} mức độ {level} đang được cập nhật..."
        ans = "Liên hệ GV để biết đáp án"
        theory = "Đang biên soạn..."
        distractors = ["Đáp án nhiễu A", "Đáp án nhiễu B", "Đáp án nhiễu C"]
        
        if concept == "nhiet_dong_luc_hoc":
            if level == "Nâng cao (VDC)":
                q = "Một máy nhiệt lý tưởng hoạt động theo chu trình Carnot giữa hai nguồn nhiệt $T_1 = 600K$ và $T_2 = 300K$. Trong mỗi chu trình, máy nhận từ nguồn nóng nhiệt lượng $Q_1 = 1200J$. Tính công toàn phần máy thực hiện và hiệu suất thực tế nếu hao phí thêm 10%."
                ans = "$A = 540J, H = 45\%$"
                distractors = ["$A = 600J, H = 50\%$", "$A = 480J, H = 40\%$", "$A = 540J, H = 50\%$"]
                theory = "Hiệu suất Carnot $H = 1 - T_2/T_1$. Công $A = H \\cdot Q_1$. Hao phí 10% công nên $A' = 0.9A$."
            else:
                q = "Nội năng của khí lý tưởng đơn nguyên tử biến thiên thế nào trong quá trình đẳng áp?"
                ans = "Tăng theo nhiệt độ"
                distractors = ["Giảm khi nhiệt độ tăng", "Không thay đổi", "Chỉ phụ thuộc áp suất"]
                theory = "Công thức nội năng: $U = \\frac{3}{2}nRT$."

        elif concept == "hat_nhan":
            if level == "Nâng cao (VDC)":
                q = "Bắn hạt $\\alpha$ vào hạt nhân $^{14}_{7}N$ đứng yên gây ra phản ứng: $^{4}_{2}He + ^{14}_{7}N \\rightarrow ^{17}_{8}O + ^{1}_{1}p$. Biết phản ứng thu nhiệt $1.21 MeV$. Hạt $\\alpha$ phải có động năng tối thiểu bao nhiêu để phản ứng xảy ra?"
                ans = "$1.56 MeV$"
                distractors = ["$1.21 MeV$", "$1.82 MeV$", "$2.15 MeV$"]
                theory = "Động năng tối thiểu $K_{min} = |Q| \\cdot \\frac{m_{\\alpha} + m_N}{m_N}$."
            else:
                q = "Đại lượng nào đặc trưng cho mức độ bền vững của hạt nhân?"
                ans = "Năng lượng liên kết riêng"
                distractors = ["Năng lượng liên kết", "Độ hụt khối", "Số khối (A)"]
                theory = "Năng lượng liên kết riêng càng lớn, hạt nhân càng bền vững."

        # Trộn đáp án đúng với các đáp án nhiễu đã được định nghĩa
        options = [ans] + distractors
        random.shuffle(options)

        dataset.append({
            "level": level,
            "question": q,
            "options": options,
            "answer": ans,
            "theory": theory,
            "concept": concept
        })
    
    return dataset

# ==========================================
# 3. THỰC THI CHÍNH (MAIN)
# ==========================================
if __name__ == "__main__":
    all_questions = []

    # Gọi hàm và thu thập dữ liệu (Tránh lỗi TypeError)
    all_questions.extend(generate_physics_dataset(100))
    all_questions.extend(generate_physics_dataset_pro(100))

    # --- ĐỊNH LUẬT NEWTON (Cơ bản) ---
    for i in range(20):
        m, a = random.randint(1, 10), random.randint(1, 10)
        F = m * a
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Một vật có khối lượng {m} kg chuyển động với gia tốc {a} m/s^2. Lực tác dụng lên vật là bao nhiêu?",
            "options": [f"{F} N", f"{F+5} N", f"{F-3} N", f"{F+10} N"],
            "answer": f"{F} N",
            "concept": "luc",
            "theory": "Định luật II Newton: F = m.a"
        })

    # --- VẬN TỐC (Cơ bản) ---
    for i in range(20):
        s, t = random.randint(20, 200), random.randint(2, 10)
        v = round(s/t, 2)
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Một vật đi được quãng đường {s} m trong {t} s. Vận tốc trung bình của vật là bao nhiêu?",
            "options": [f"{v} m/s", f"{v+2} m/s", f"{v+5} m/s", f"{v-1} m/s"],
            "answer": f"{v} m/s",
            "concept": "van_toc",
            "theory": "Vận tốc v = s/t"
        })

    # ==========================================
    # CHỦ ĐỀ: TỪ TRƯỜNG (4 LEVEL)
    # ==========================================
    for i in range(25):
        # --- CƠ BẢN (Đơn vị và khái niệm) ---
        all_questions.append({
            "level": "Cơ bản",
            "question": "Đơn vị của cảm ứng từ trong hệ SI là:",
            "options": ["Tesla (T)", "Weber (Wb)", "Vôn (V)", "Ampe (A)"],
            "answer": "Tesla (T)", "concept": "tu_truong"
        })

        # --- TRUNG BÌNH (Lực từ trên dây dẫn) ---
        I, L, B = random.randint(2, 5), random.randint(1, 2), round(random.uniform(0.1, 0.5), 2)
        F = round(B * I * L, 2)
        all_questions.append({
            "level": "Trung bình",
            "question": f"Một dây dẫn thẳng dài {L}m đặt vuông góc với từ trường đều $B = {B}T$. Dòng điện qua dây là {I}A. Lực từ tác dụng lên dây là:",
            "options": [f"{F} N", f"{F*2} N", f"{F/2} N", "0 N"],
            "answer": f"{F} N", "concept": "tu_truong"
        })

        # --- KHÓ (Lực Lorentz) ---
        v = 2 # 10^6 m/s
        q = 1.6 # 10^-19 C
        B_val = 0.5
        F_L = round(q * v * B_val, 2) # * 10^-13
        all_questions.append({
            "level": "Khó",
            "question": f"Một hạt proton ($q = 1.6 \cdot 10^{{-19}}C$) bay vào từ trường $B = 0.5T$ với vận tốc $v = 2 \cdot 10^6 m/s$ theo phương vuông góc. Lực Lorentz là:",
            "options": [f"${F_L} \cdot 10^{{-13}} N$", f"${F_L*10} \cdot 10^{{-13}} N$", "0 N", f"${F_L} \cdot 10^{{-19}} N$"],
            "answer": f"${F_L} \cdot 10^{{-13}} N$", "concept": "tu_truong"
        })

        # --- NÂNG CAO VDC (Chuyển động trong từ trường) ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Một hạt điện tích chuyển động tròn đều trong từ trường đều. Nếu vận tốc hạt tăng gấp đôi và cảm ứng từ giảm một nửa thì bán kính quỹ đạo thay đổi thế nào?",
            "options": ["Tăng 4 lần", "Không đổi", "Giảm 4 lần", "Tăng 2 lần"],
            "answer": "Tăng 4 lần", "concept": "tu_truong",
            "theory": "Công thức bán kính quỹ đạo: R = mv / (|q|B). v tăng 2, B giảm 0.5 => R tăng 4."
        })
    # ==========================================
    # CHỦ ĐỀ: VẬT LÝ HẠT NHÂN (4 LEVEL)
    # ==========================================
    for i in range(25):
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": "Hạt nhân $^{235}_{92}U$ có bao nhiêu neutron?",
            "options": ["143", "92", "235", "327"],
            "answer": "143", "concept": "hat_nhan"
        })

        # --- TRUNG BÌNH (Chu kỳ bán rã) ---
        T = 8 # ngày
        t = 24 # ngày
        rem = 100 / (2**(t/T))
        all_questions.append({
            "level": "Trung bình",
            "question": f"Chất phóng xạ có chu kỳ bán rã {T} ngày. Sau {t} ngày, lượng chất còn lại chiếm bao nhiêu % khối lượng ban đầu?",
            "options": [f"{rem}%", "25%", "50%", "10%"],
            "answer": f"{rem}%", "concept": "hat_nhan"
        })

        # --- KHÓ (Năng lượng liên kết) ---
        all_questions.append({
            "level": "Khó",
            "question": "Năng lượng liên kết riêng của một hạt nhân được tính bằng:",
            "options": ["Năng lượng liên kết chia cho tổng số nucleon", "Năng lượng liên kết chia cho số proton", "Độ hụt khối nhân với c bình phương", "Năng lượng nghỉ của hạt nhân"],
            "answer": "Năng lượng liên kết chia cho tổng số nucleon", "concept": "hat_nhan"
        })

        # --- NÂNG CAO VDC (Phản ứng hạt nhân) ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Cho phản ứng nhiệt hạch: $^2_1D + ^3_1T \\rightarrow ^4_2He + ^1_0n$. Biết năng lượng liên kết riêng của D, T, He lần lượt là 1.1 MeV; 2.8 MeV và 7.0 MeV. Năng lượng tỏa ra là:",
            "options": ["17.6 MeV", "15.3 MeV", "20.1 MeV", "18.9 MeV"],
            "answer": "17.6 MeV", "concept": "hat_nhan",
            "theory": "Q = (lk_sau) - (lk_truoc) = (7.0*4) - (1.1*2 + 2.8*3) = 28 - 10.6 = 17.4 (xấp xỉ 17.6)."
        })

    # ==========================================
    # CHỦ ĐỀ: KHÍ LÝ TƯỞNG (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": "Trong quá trình đẳng nhiệt của một lượng khí lý tưởng, áp suất và thể tích liên hệ thế nào?",
            "options": ["Tỉ lệ nghịch", "Tỉ lệ thuận", "Luôn bằng nhau", "Không liên quan"],
            "answer": "Tỉ lệ nghịch", "concept": "khi_ly_tuong"
        })

        # --- TRUNG BÌNH (Đẳng áp) ---
        V1 = 2
        T1 = 300 # K
        T2 = 600 # K
        V2 = V1 * (T2/T1)
        all_questions.append({
            "level": "Trung bình",
            "question": f"Một khối khí có thể tích {V1} lít ở {T1}K. Nếu nung nóng đẳng áp lên {T2}K thì thể tích là:",
            "options": [f"{V2} lít", "1 lít", "3 lít", "4 lít"],
            "answer": f"{V2} lít", "concept": "khi_ly_tuong"
        })

        # --- KHÓ (Phương trình Clapeyron-Mendeleev) ---
        all_questions.append({
            "level": "Khó",
            "question": "Hằng số khí lý tưởng R có giá trị và đơn vị nào sau đây?",
            "options": ["8.31 J/(mol.K)", "0.082 J/(mol.K)", "8.31 atm.l/(mol.K)", "1.38 \cdot 10^{-23} J/K"],
            "answer": "8.31 J/(mol.K)", "concept": "khi_ly_tuong"
        })

        # --- NÂNG CAO VDC (Hỗn hợp khí) ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Một bình dung tích 20 lít chứa hỗn hợp khí gồm 2g Hidro và 8g Heli ở 27°C. Áp suất hỗn hợp khí là:",
            "options": ["3.74 atm", "1.25 atm", "5.00 atm", "2.48 atm"],
            "answer": "3.74 atm", "concept": "khi_ly_tuong",
            "theory": "n_tong = n_H2 + n_He = 2/2 + 8/4 = 3 mol. P = nRT/V = 3 * 0.082 * 300 / 20."
        })
    # ==========================================
    # CHỦ ĐỀ: NHIỆT ĐỘNG LỰC HỌC (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": "Công thức của Nguyên lý I Nhiệt động lực học là:",
            "options": ["$\Delta U = Q + A$", "$\Delta U = Q - A$", "$Q = \Delta U + A$", "A = Q + \Delta U"],
            "answer": "$\Delta U = Q + A$", "concept": "nhiet_dong_luc_hoc"
        })

        # --- TRUNG BÌNH ---
        Q_in = 100
        A_out = 40
        dU = Q_in - A_out
        all_questions.append({
            "level": "Trung bình",
            "question": f"Hệ nhận nhiệt lượng {Q_in}J và thực hiện công {A_out}J. Độ biến thiên nội năng của hệ là:",
            "options": [f"{dU} J", "140 J", "-60 J", "100 J"],
            "answer": f"{dU} J", "concept": "nhiet_dong_luc_hoc"
        })

        # --- KHÓ (Hiệu suất máy nhiệt) ---
        T_h = 500
        T_c = 300
        H = (1 - T_c/T_h) * 100
        all_questions.append({
            "level": "Khó",
            "question": f"Hiệu suất cực đại của một máy nhiệt hoạt động giữa nguồn nóng {T_h}K và nguồn lạnh {T_c}K là:",
            "options": [f"{H}%", "60%", "20%", "50%"],
            "answer": f"{H}%", "concept": "nhiet_dong_luc_hoc"
        })

        # --- NÂNG CAO VDC (Chu trình phức hợp) ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Trong một chu trình kín của khí lý tưởng, tổng nhiệt lượng hệ nhận được là 2000J. Công mà hệ thực hiện trong cả chu trình là:",
            "options": ["2000 J", "0 J", "1000 J", "Không thể xác định"],
            "answer": "2000 J", "concept": "nhiet_dong_luc_hoc",
            "theory": "Trong chu trình kín, Delta U = 0 nên A = Q."
        })

    # --- GHI FILE JSON ---
    os.makedirs("dataset", exist_ok=True)
    with open("dataset/physics.json", "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)

    print("-" * 30)
    print(f"THÀNH CÔNG: Đã tạo {len(all_questions)} câu hỏi.")
    print(f"Đường dẫn:ai_exam_project/dataset/physics.json")
    print("-" * 30)