import json
import random
import os
from sympy import symbols, diff, integrate, sin, cos, exp, log, latex, pi, simplify

# --- HÀM 1: SINH TOÁN CƠ BẢN/TRUNG BÌNH ---
def generate_math_dataset(num_questions=100):
    x = symbols('x')
    dataset = []
    for i in range(num_questions):
        level = random.choice(["Trung bình", "Khó"])
        concept_choice = random.choice(["dao_ham", "tich_phan", "logarit", "nguyen_ham"])
        
        if concept_choice == "dao_ham":
            if level == "Trung bình":
                f = random.randint(2, 5)*x**random.randint(2, 4) + random.randint(1, 10)
            else:
                f = sin(random.randint(2, 4)*x) * exp(random.randint(1, 3)*x)
            ans = diff(f, x)
            q_text = f"Tính đạo hàm của hàm số $f(x) = {latex(f)}$"
            correct_ans = f"${latex(ans)}$"
        elif concept_choice == "tich_phan":
            a_val, b_val = random.randint(0, 1), random.randint(2, 3)
            f = x * exp(x) if level == "Khó" else random.randint(1, 5)*x
            ans_val = integrate(f, (x, a_val, b_val))
            q_text = f"Tính tích phân $I = \\int_{{{a_val}}}^{{{b_val}}} ({latex(f)}) dx$"
            correct_ans = f"${latex(simplify(ans_val))}$"
        else:
            continue

        options = [correct_ans, "$0$", "$\\pi$", "$-1$"]
        random.shuffle(options)
        dataset.append({
            "level": level, "question": q_text, "options": options,
            "answer": correct_ans, "concept": concept_choice
        })
    return dataset

# --- HÀM 2: SINH TOÁN NÂNG CAO (VDC) ---
def generate_math_dataset_pro(num_questions=100):
    x = symbols('x')
    dataset = []
    for i in range(num_questions):
        level = "Nâng cao (VDC)"
        concept = random.choice(["dao_ham", "tich_phan"])
        if concept == "dao_ham":
            f = exp(sin(x**2 + 1)) * log(x + 1)
            ans = diff(f, x)
            q_text = f"Tính đạo hàm của hàm số bậc cao: $f(x) = {latex(f)}$"
            correct_ans = f"${latex(ans)}$"
        else:
            f = x**2 * exp(x)
            ans_val = integrate(f, (x, 0, 1))
            q_text = f"Tính giá trị biểu thức tích phân $I = \\int_{{0}}^{{1}} {latex(f)} dx$"
            correct_ans = f"${latex(simplify(ans_val))}$"

        options = [correct_ans, "$e-1$", "$0$", "$1$"]
        random.shuffle(options)
        dataset.append({
            "level": level, "question": q_text, "options": options,
            "answer": correct_ans, "concept": concept,
            "theory": "Sử dụng các quy tắc đạo hàm/tích phân hàm hợp nâng cao."
        })
    return dataset

if __name__ == "__main__":
    file_path = "dataset/math.json"
    os.makedirs("dataset", exist_ok=True)
    all_questions = []

    # 1. Gọi các hàm sinh tự động (Đã có level)
    all_questions.extend(generate_math_dataset(100))
    all_questions.extend(generate_math_dataset_pro(100))

    # 2. Cập nhật các vòng lặp thủ công - THÊM LEVEL
    
    # ==========================================
    # CHỦ ĐỀ: ĐẠO HÀM (ĐỦ 4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN (Quy tắc tính) ---
        n = random.randint(3, 7)
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Tính đạo hàm của hàm số $y = x^{{{n}}} + 5x$.",
            "options": [f"${n}x^{{{n-1}}} + 5$", f"${n}x^{{{n}}} + 5$", f"$x^{{{n-1}}} + 5$", f"${n}x^{{{n-1}}}$"],
            "answer": f"${n}x^{{{n-1}}} + 5$", "concept": "dao_ham"
        })

        # --- TRUNG BÌNH (Đạo hàm hàm hợp) ---
        u_val = random.randint(2, 4)
        all_questions.append({
            "level": "Trung bình",
            "question": f"Đạo hàm của hàm số $y = \\sin({u_val}x)$ là:",
            "options": [f"${u_val}\\cos({u_val}x)$", f"$\\cos({u_val}x)$", f"$-{u_val}\\cos({u_val}x)$", f"${u_val}\\sin({u_val}x)$"],
            "answer": f"${u_val}\\cos({u_val}x)$", "concept": "dao_ham"
        })

        # --- KHÓ (Cực trị) ---
        a = random.randint(1, 3) # y = x^2 - 2ax
        all_questions.append({
            "level": "Khó",
            "question": f"Tìm điểm cực tiểu của hàm số $y = x^2 - {2*a}x + 1$.",
            "options": [f"$x = {a}$", f"$x = -{a}$", f"$x = 0$", f"$x = {2*a}$"],
            "answer": f"$x = {a}$", "concept": "dao_ham"
        })

        # --- NÂNG CAO VDC (Biện luận đơn điệu) ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": f"Tìm m để hàm số $y = \\frac{{1}}{{3}}x^3 - mx^2 + (m^2 - m + 1)x$ đồng biến trên $\\mathbb{{R}}$.",
            "options": ["$m \\le 1$", "$m < 1$", "$m \\ge 1$", "$m \\in \\mathbb{{R}}$"],
            "answer": "$m \\le 1$", "concept": "dao_ham",
            "theory": "Hàm bậc 3 đồng biến trên R khi y' >= 0 với mọi x, tương đương Delta' của y' <= 0."
        })

    # ==========================================
    # CHỦ ĐỀ: NGUYÊN HÀM (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN ---
        n = random.randint(2, 5)
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Tìm nguyên hàm của hàm số $f(x) = x^{{{n}}}$.",
            "options": [f"$\\frac{{x^{{{n+1}}}}}{{{n+1}}} + C$", f"${n}x^{{{n-1}}} + C$", f"$x^{{{n+1}}} + C$", f"$\\frac{{x^{{{n}}}}}{{{n}}} + C$"],
            "answer": f"$\\frac{{x^{{{n+1}}}}}{{{n+1}}} + C$", "concept": "nguyen_ham"
        })

        # --- TRUNG BÌNH ---
        all_questions.append({
            "level": "Trung bình",
            "question": "Nguyên hàm của hàm số $f(x) = e^{2x}$ là:",
            "options": ["$\\frac{1}{2}e^{2x} + C$", "$2e^{2x} + C$", "$e^{2x} + C$", "$e^x + C$"],
            "answer": "$\\frac{1}{2}e^{2x} + C$", "concept": "nguyen_ham"
        })

        # --- KHÓ ---
        all_questions.append({
            "level": "Khó",
            "question": "Tính nguyên hàm $F(x) = \\int x \\cos(x) dx$.",
            "options": ["$x \\sin(x) + \\cos(x) + C$", "$x \\sin(x) - \\cos(x) + C$", "$-x \\sin(x) + \\cos(x) + C$", "$\\sin(x) + x \\cos(x) + C$"],
            "answer": "$x \\sin(x) + \\cos(x) + C$", "concept": "nguyen_ham"
        })

        # --- NÂNG CAO VDC ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Tìm nguyên hàm $F(x)$ của hàm số $f(x) = \\frac{2x+1}{(x+1)^2}$ thỏa mãn $F(0) = 1$.",
            "options": ["$2\\ln|x+1| + \\frac{1}{x+1}$", "$2\\ln|x+1| - \\frac{1}{x+1} + 2$", "$\\ln|x+1|^2 + 1$", "$2\\ln|x+1| + 1$"],
            "answer": "$2\\ln|x+1| + \\frac{1}{x+1}$", "concept": "nguyen_ham"
        })

    # ==========================================
    # CHỦ ĐỀ: MŨ VÀ LOGARIT (ĐỦ 4 LEVEL)
    # ==========================================
    for i in range(25):
        # --- LEVEL 1: CƠ BẢN (Nhận biết công thức) ---
        a_base = random.choice([2, 3, 5])
        exp_val = random.randint(2, 4)
        res_val = a_base ** exp_val
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Giá trị của biểu thức $P = \\log_{{{a_base}}}({res_val})$ là:",
            "options": [str(exp_val), str(a_base), str(res_val), "1"],
            "answer": str(exp_val), "concept": "logarit"
        })

        # --- LEVEL 2: TRUNG BÌNH (Biến đổi cơ bản) ---
        # log(a) + log(b) = log(ab)
        x_val = random.randint(2, 5)
        y_val = random.randint(2, 5)
        total_log = x_val * y_val
        all_questions.append({
            "level": "Trung bình",
            "question": f"Cho $\\log_a(x) = {x_val}$ và $\\log_a(y) = {y_val}$. Tính giá trị của $\\log_a(x^2 \\cdot y)$.",
            "options": [str(2*x_val + y_val), str(x_val + y_val), str(x_val * y_val), str(x_val**2 + y_val)],
            "answer": str(2*x_val + y_val), "concept": "logarit"
        })

        # --- LEVEL 3: KHÓ (Phương trình mũ/log chứa ẩn) ---
        # a^(x^2 - 4) = 1 => x = 2, -2
        base_k = random.randint(2, 7)
        all_questions.append({
            "level": "Khó",
            "question": f"Tìm tập nghiệm của phương trình ${base_k}^{{x^2 - 4}} = 1$.",
            "options": ["$\\{2; -2\\}$", "$\\{2\\}$", "$\\{4; -4\\}$", "$\\{0\\}$"],
            "answer": "$\\{2; -2\\}$", "concept": "logarit"
        })

        # --- LEVEL 4: NÂNG CAO (VDC - Biện luận tham số m) ---
        m_val = random.randint(1, 5)
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": f"Tìm số giá trị nguyên của tham số $m \\in [-10; 10]$ để phương trình $\\log_3^2(x) - (m+{m_val})\\log_3(x) + {m_val}m = 0$ có hai nghiệm phân biệt $x_1, x_2$ thỏa mãn $x_1 \\cdot x_2 = 81$.",
            "options": ["1", "2", "10", "Vô số"],
            "answer": "1", "concept": "logarit",
            "theory": "Sử dụng định lý Vi-et cho phương trình bậc hai đối với ẩn t = log_3(x). log_3(x1) + log_3(x2) = log_3(x1.x2) = log_3(81) = 4."
        })

    # ==========================================
    # CHỦ ĐỀ: CẤP SỐ CỘNG & CẤP SỐ NHÂN (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN (Nhận biết CSC) ---
        a1 = random.randint(1, 10)
        d = random.randint(2, 5)
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Cho cấp số cộng có $u_1 = {a1}$ và công sai $d = {d}$. Tính $u_2$.",
            "options": [str(a1 + d), str(a1 + 2*d), str(a1 - d), str(a1 * d)],
            "answer": str(a1 + d), "concept": "cap_so_cong"
        })

        # --- TRUNG BÌNH (Công thức số hạng tổng quát) ---
        n = random.randint(5, 10)
        un = a1 + (n-1)*d
        all_questions.append({
            "level": "Trung bình",
            "question": f"Cho cấp số cộng có $u_1 = {a1}$ và $d = {d}$. Tìm số hạng thứ {n}.",
            "options": [str(un), str(un + d), str(un - d), str(a1 + n*d)],
            "answer": str(un), "concept": "cap_so_cong"
        })

        # --- KHÓ (Cấp số nhân) ---
        u1_q = random.randint(1, 3)
        q = 2
        n_q = 5
        un_q = u1_q * (q**(n_q-1))
        all_questions.append({
            "level": "Khó",
            "question": f"Cho cấp số nhân có $u_1 = {u1_q}$ và công bội $q = {q}$. Tìm $u_{{{n_q}}}$.",
            "options": [str(un_q), str(un_q * q), str(un_q / q), str(u1_q + (n_q-1)*q)],
            "answer": str(un_q), "concept": "cap_so_nhan"
        })

        # --- NÂNG CAO VDC (Tổng dãy số) ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Cho cấp số cộng $(u_n)$ thỏa mãn $u_1 + u_5 = 20$ và $u_3 + u_{10} = 35$. Tính tổng 20 số hạng đầu tiên $S_{20}$.",
            "options": ["530", "510", "490", "600"],
            "answer": "530", "concept": "cap_so_cong",
            "theory": "Giải hệ phương trình tìm u1 và d, sau đó áp dụng công thức Sn = [2u1 + (n-1)d]*n/2."
        })

    # ==========================================
    # CHỦ ĐỀ: XÁC SUẤT (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": "Gieo một con xúc xắc cân đối. Xác suất xuất hiện mặt có số chấm là số chẵn?",
            "options": ["1/2", "1/3", "1/6", "2/3"],
            "answer": "1/2", "concept": "xac_suat"
        })

        # --- TRUNG BÌNH ---
        all_questions.append({
            "level": "Trung bình",
            "question": "Một hộp chứa 5 bi đỏ và 3 bi xanh. Lấy ngẫu nhiên 2 bi. Tính xác suất lấy được 2 bi đỏ.",
            "options": ["5/14", "10/28", "25/64", "1/2"],
            "answer": "5/14", "concept": "xac_suat"
        })

        # --- KHÓ ---
        all_questions.append({
            "level": "Khó",
            "question": "Xác suất bắn trúng mục tiêu của một xạ thủ là 0.8. Xạ thủ bắn 3 viên. Tính xác suất để có ít nhất 1 viên trúng mục tiêu.",
            "options": ["0.992", "0.512", "0.8", "0.2"],
            "answer": "0.992", "concept": "xac_suat"
        })

        # --- NÂNG CAO VDC ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Chọn ngẫu nhiên 3 số từ tập $S = \{1, 2, ..., 20\}$. Tính xác suất để 3 số được chọn lập thành một cấp số cộng.",
            "options": ["3/38", "1/114", "7/190", "11/1140"],
            "answer": "3/38", "concept": "xac_suat"
        })
    # ==========================================
    # CHỦ ĐỀ: SỐ PHỨC (ĐỦ 4 LEVEL)
    # ==========================================
    for i in range(20):
        a, b = random.randint(1, 5), random.randint(1, 5)
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Cho số phức $z = {a} - {b}i$. Môđun của số phức $z$ là:",
            "options": [f"$\\sqrt{{{a**2 + b**2}}}$", f"{a**2 + b**2}", f"{a+b}", f"$\\sqrt{{{a**2 - b**2}}}$"],
            "answer": f"$\\sqrt{{{a**2 + b**2}}}$", "concept": "so_phuc"
        })

        # --- TRUNG BÌNH ---
        all_questions.append({
            "level": "Trung bình",
            "question": f"Cho $z_1 = 1 + i$ và $z_2 = {a} - i$. Tính $z_1 + z_2$.",
            "options": [f"${a+1}$", f"${a} + 2i$", f"${a+1} + i$", f"${a} - i$"],
            "answer": f"${a+1}$", "concept": "so_phuc"
        })

        # --- KHÓ ---
        all_questions.append({
            "level": "Khó",
            "question": f"Tìm tập hợp điểm biểu diễn số phức $z$ thỏa mãn $|z - i| = 2$.",
            "options": ["Đường tròn tâm $I(0,1)$ bán kính $R=2$", "Đường thẳng $y=1$", "Đường tròn tâm $I(0,-1)$ bán kính $R=2$", "Hình vuông"],
            "answer": "Đường tròn tâm $I(0,1)$ bán kính $R=2$", "concept": "so_phuc"
        })

        # --- NÂNG CAO VDC ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": f"Trong các số phức $z$ thỏa mãn $|z - 2 - 4i| = |z - 2i|$, tìm giá trị nhỏ nhất của $|z|$.",
            "options": [f"$\\sqrt{{5}}$", f"$2\\sqrt{{5}}$", "2", "4"],
            "answer": f"$\\sqrt{{5}}$", "concept": "so_phuc",
            "theory": "Tập hợp z là đường trung trực của đoạn thẳng nối hai điểm. Khoảng cách nhỏ nhất từ O đến đường thẳng đó là đường cao."
        })

    # ==========================================
    # CHỦ ĐỀ: TIỆM CẬN (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN (Nhận biết tiệm cận ngang) ---
        a = random.randint(2, 6)
        b = random.randint(1, 9)
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Tìm tiệm cận ngang của đồ thị hàm số $y = \\frac{{{a}x - 1}}{{x + {b}}}$.",
            "options": [f"$y = {a}$", f"$y = 1$", f"$x = -{b}$", f"$y = -{a}$"],
            "answer": f"$y = {a}$", "concept": "tiem_can"
        })

        # --- TRUNG BÌNH (Nhận biết tiệm cận đứng) ---
        c = random.randint(1, 5)
        all_questions.append({
            "level": "Trung bình",
            "question": f"Đồ thị hàm số $y = \\frac{{2x + 3}}{{{c}x - {c*2}}}$ có đường tiệm cận đứng là:",
            "options": ["$x = 2$", "$x = -2$", "$y = 2/c$", "$x = 0$"],
            "answer": "$x = 2$", "concept": "tiem_can"
        })

        # --- KHÓ (Hàm chứa căn thức hoặc trị tuyệt đối) ---
        all_questions.append({
            "level": "Khó",
            "question": "Tổng số đường tiệm cận đứng và tiệm cận ngang của đồ thị hàm số $y = \\frac{\\sqrt{x+1}-1}{x^2 - x}$ là:",
            "options": ["2", "1", "3", "0"],
            "answer": "2", "concept": "tiem_can",
            "theory": "Xét tập xác định, tính giới hạn tại vô cực (TCN) và giới hạn tại các điểm làm mẫu bằng 0 (TCĐ)."
        })

        # --- NÂNG CAO VDC (Biện luận tham số m) ---
        m_val = random.randint(1, 3)
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": f"Tìm tất cả các giá trị thực của tham số $m$ để đồ thị hàm số $y = \\frac{{x + 1}}{{x^2 - 2mx + 4}}$ có đúng hai đường tiệm cận đứng.",
            "options": ["$|m| > 2$ và $m \\neq -2.5$", "$|m| > 2$", "$m > 2$", "$m < -2$"],
            "answer": "$|m| > 2$ và $m \\neq -2.5$", "concept": "tiem_can",
            "theory": "Để có 2 TCĐ thì mẫu số phải có 2 nghiệm phân biệt và các nghiệm đó không được triệt tiêu với tử số."
        })

    # ==========================================
    # CHỦ ĐỀ: HÌNH HỌC OXYZ (ĐỦ 4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": f"Trong không gian Oxyz, tọa độ hình chiếu của điểm $M(1, 2, 3)$ lên mặt phẳng $(Oxy)$ là:",
            "options": ["$(1, 2, 0)$", "$(0, 0, 3)$", "$(1, 0, 3)$", "$(0, 2, 3)$"],
            "answer": "$(1, 2, 0)$", "concept": "hinh_hoc_oxyz"
        })

        # --- TRUNG BÌNH ---
        all_questions.append({
            "level": "Trung bình",
            "question": f"Mặt phẳng đi qua $A(1,0,0), B(0,2,0), C(0,0,3)$ có phương trình là:",
            "options": ["$\\frac{x}{1} + \\frac{y}{2} + \\frac{z}{3} = 1$", "$x + 2y + 3z = 1$", "$x + y + z = 6$", "$x + 2y + 3z = 0$"],
            "answer": "$\\frac{x}{1} + \\frac{y}{2} + \\frac{z}{3} = 1$", "concept": "hinh_hoc_oxyz"
        })

        # --- KHÓ ---
        all_questions.append({
            "level": "Khó",
            "question": f"Tính khoảng cách từ điểm $M(1, 2, 1)$ đến mặt phẳng $(P): 2x - 2y + z + 3 = 0$.",
            "options": ["$2/3$", "$2$", "$4/3$", "$1$"],
            "answer": "$2/3$", "concept": "hinh_hoc_oxyz"
        })

        # --- NÂNG CAO VDC ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Viết phương trình đường thẳng $d$ đi qua $A(1,2,3)$ vuông góc với $d_1$ và cắt $d_2$.",
            "options": ["Dạng chính tắc A", "Dạng chính tắc B", "Dạng chính tắc C", "Dạng chính tắc D"],
            "answer": "Dạng chính tắc A", "concept": "hinh_hoc_oxyz",
            "theory": "Sử dụng tích có hướng để tìm vecto chỉ phương và điều kiện cắt nhau của hai đường thẳng."
        })

    # ==========================================
    # CHỦ ĐỀ: CỰC TRỊ HÀM SỐ (4 LEVEL)
    # ==========================================
    for i in range(20):
        # --- CƠ BẢN ---
        all_questions.append({
            "level": "Cơ bản",
            "question": "Điểm cực trị của đồ thị hàm số là gì?",
            "options": ["Điểm mà tại đó đạo hàm đổi dấu", "Điểm có giá trị y lớn nhất", "Điểm có đạo hàm bằng 0", "Giao điểm với trục tung"],
            "answer": "Điểm mà tại đó đạo hàm đổi dấu", "concept": "dao_ham"
        })

        # --- TRUNG BÌNH ---
        a = random.randint(1, 3) # y = x^2 - 2ax
        all_questions.append({
            "level": "Trung bình",
            "question": f"Hàm số $y = x^2 - {2*a}x + 5$ đạt cực tiểu tại $x$ bằng:",
            "options": [str(a), str(-a), "0", str(2*a)],
            "answer": str(a), "concept": "dao_ham"
        })

        # --- KHÓ ---
        all_questions.append({
            "level": "Khó",
            "question": "Tìm số điểm cực trị của hàm số $y = x^4 - 2x^2 + 3$.",
            "options": ["3", "1", "2", "0"],
            "answer": "3", "concept": "dao_ham"
        })

        # --- NÂNG CAO VDC ---
        all_questions.append({
            "level": "Nâng cao (VDC)",
            "question": "Tìm m để hàm số $y = x^3 - 3mx^2 + 3(m^2-1)x + 1$ có hai điểm cực trị nằm về hai phía của trục tung.",
            "options": ["$|m| < 1$", "$m > 1$", "$m < -1$", "$m = 0$"],
            "answer": "$|m| < 1$", "concept": "dao_ham",
            "theory": "Hai điểm cực trị nằm về 2 phía trục tung khi tích hai cực trị x1.x2 < 0 (c/a < 0)."
        })

    # 3. Ghi file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)

    print(f"Thành công! Đã tạo {len(all_questions)} câu hỏi Toán có đầy đủ Level.")