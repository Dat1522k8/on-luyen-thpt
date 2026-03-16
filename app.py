from flask import Flask, render_template, jsonify, request
import json
import random
from ai_tutor import phan_tich_hoc_tap, hoi_ai

app = Flask(__name__)

de_hien_tai = []

goi_y_hoc = {
    "dao_ham":"Ôn quy tắc đạo hàm (x^n)' = n*x^(n-1)",
    "nguyen_ham":"Ôn nguyên hàm ∫x^n dx = x^(n+1)/(n+1) + C",
    "logarit":"Ôn quy tắc logarit log(ab)=log a + log b",
    "cap_so_cong":"Ôn công thức a_n = a1 + (n-1)d",
    "cap_so_nhan":"Ôn công thức a_n = a1*q^(n-1)",
    "xac_suat":"Ôn xác suất có điều kiện và Bayes",
    "luc":"Ôn định luật Newton F = m.a",
    "dien_ap":"Ôn định luật Ohm U = I.R",
    "tu_truong":"Ôn lực Lorentz",
    "khi_ly_tuong":"Ôn phương trình khí lý tưởng",
    "nhiet_hoc":"Ôn nguyên lý nhiệt động lực học",
    "hat_nhan":"Ôn phản ứng hạt nhân"
}

def tai_du_lieu(mon):
    try:
        filename = "dataset/math.json" if mon == "toan" else "dataset/physics.json"
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Lỗi dataset:", e)
    return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/concepts")
def concepts():
    mon = request.args.get("mon")
    if mon == "toan":
        concepts = ["dao_ham", "nguyen_ham", "logarit", "cap_so_cong", "cap_so_nhan", "nhan_xac_xuat", "xac_suat_co_dieu_kien", "xac_suat_toan_phan_va_bayes", "xac_suat", "vector", "toa_do_hoa_hinh_hoc", "tich_phan", "so_phuc", "tiem_can"]
    else:
        concepts = ["dien_ap", "tu_truong", "khi_ly_tuong", "nhiet_hoc", "hat_nhan", "mo_men_luc", "pttt", "vat_ly_nhiet"]
    return jsonify(concepts)

@app.route("/tao_de")
def tao_de():
    global de_hien_tai
    mon = request.args.get("mon")
    concept = request.args.get("concept")
    so_cau = int(request.args.get("so_cau", 10))
    
    # 1. Tải toàn bộ dữ liệu (vốn dĩ đã là câu khó)
    data = tai_du_lieu(mon)
    
    # 2. Lọc theo chủ đề (concept) nếu người dùng yêu cầu cụ thể
    if concept and concept != "all":
        data = [q for q in data if q.get("concept") == concept]
    
    # 3. Kiểm tra xem có dữ liệu không
    if not data: 
        return jsonify({"de": [], "message": "Không tìm thấy câu hỏi!"})

    # 4. Lấy ngẫu nhiên số lượng câu (đảm bảo không lấy quá số câu hiện có)
    so_luong_lay = min(so_cau, len(data))
    de_moi = random.sample(data, so_luong_lay)
    
    # 5. Trộn đề cho khách quan
    random.shuffle(de_moi)
    de_hien_tai = de_moi
    
    return jsonify({"de": de_hien_tai})

@app.route("/nop_bai", methods=["POST"])
def nop_bai():
    data = request.json
    cau_tra_loi = data["cau_tra_loi"]
    score, results, weak = 0, [], {}
    for q, ans in zip(de_hien_tai, cau_tra_loi):
        dung = (ans == q["answer"])
        if dung: score += 1
        else:
            c = q.get("concept", "unknown"); weak[c] = weak.get(c, 0) + 1
        results.append({"cau_hoi": q["question"], "tra_loi_cua_ban": ans, "dap_an_dung": q["answer"], "dung": dung})
    return jsonify({"diem": score, "phan_tram": round(score/len(de_hien_tai)*100, 2), "ket_qua": results, "goi_y": [goi_y_hoc[k] for k in weak if k in goi_y_hoc]})

@app.route("/ai_lo_trinh", methods=["POST"])
def ai_lo_trinh():
    data = request.json
    cau_sai = data.get("cau_sai", [])
    result = phan_tich_hoc_tap(cau_sai)
    return jsonify({"answer": result})

@app.route("/chat_ai", methods=["POST"])
def chat_ai():
    data = request.json
    msg = data.get("message", "")
    ctx = data.get("context")
    
    if ctx:
        # Nhắc nhở AI tập trung vào câu hỏi cụ thể của người dùng thay vì giải thích chung chung
        prompt = f"""
        Ngữ cảnh bài tập:
        - Câu hỏi: {ctx['question']}
        - Học sinh đã chọn: {ctx['student_choice']}
        - Đáp án đúng là: {ctx['correct_answer']}
        
        Yêu cầu mới từ học sinh: {msg}
        (Hãy trả lời trực tiếp câu hỏi này dựa trên ngữ cảnh bài tập trên)
        """
    else:
        prompt = f"Trò chuyện tự do: {msg}"
        
    return jsonify({"answer": hoi_ai(prompt)})
if __name__ == "__main__":
    # Render sẽ tự cấp một cổng (Port) thông qua biến môi trường
    # Nếu không có (chạy ở máy), nó sẽ dùng cổng 5000
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)