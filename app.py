from flask import Flask, render_template, jsonify, request
import json
import random
import os
import csv
from datetime import datetime
# Import các hàm từ file ai_tutor của chúng ta
from ai_tutor import hoi_ai, phan_tich_hoc_tap

app = Flask(__name__)

# Lưu trữ đề hiện tại để đối chiếu khi nộp bài
de_hien_tai = []

# Gợi ý học tập
goi_y_hoc = {
    "dao_ham": "Ôn quy tắc đạo hàm (x^n)' = n*x^(n-1)",
    "nguyen_ham": "Ôn nguyên hàm ∫x^n dx = x^(n+1)/(n+1) + C",
    "logarit": "Ôn quy tắc logarit log(ab)=log a + log b",
    "cap_so_cong": "Ôn công thức a_n = a1 + (n-1)d",
    "cap_so_nhan": "Ôn công thức a_n = a1*q^(n-1)",
    "xac_suat": "Ôn xác suất có điều kiện và Bayes",
    "Vật lý nhiệt": "Ôn lại nội năng và các nguyên lý nhiệt động lực học.",
    "Các đẳng quá trình": "Ghi nhớ các định luật Boyle, Charles và Gay-Lussac.",
    "Từ trường": "Xem lại quy tắc bàn tay trái và công thức lực Lorentz.",
    "Vật lý hạt nhân": "Ôn tập định luật bảo toàn số khối và chu kỳ bán rã.",
    "Điện xoay chiều": "Ghi nhớ công thức tính tổng trở Z và các hiện tượng cộng hưởng.",
    "Sóng điện từ": "Ôn lại tính chất của các loại sóng vô tuyến và cấu tạo máy thu phát.",
    "Sóng cơ": "Xem lại định nghĩa bước sóng và phương trình truyền sóng."
}

def tai_du_lieu(mon):
    try:
        filename = "dataset/math.json" if mon == "toan" else "dataset/physics.json"
        if not os.path.exists(filename):
            return []
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
        concepts = ["hàm số và đồ thị", "nguyên hàm tích phân", "hình học không gian", "khối tròn xoay", "tọa độ không gian", "số mũ và logarit", "số phức", "tổ hợp và xác suất", "đạo hàm", "cấp số cộng", "cấp số nhân", "tiệm cận"]
    else:
        concepts = ["Khí lí tưởng", "Vật lý hạt nhân", "Từ trường", "Vật lí nhiệt"]
    return jsonify(concepts)

@app.route("/tao_de")
def tao_de():
    global de_hien_tai
    mon = request.args.get("mon")
    concept = request.args.get("concept")
    so_cau = int(request.args.get("so_cau", 10))
    
    data = tai_du_lieu(mon)
    if concept and concept != "all":
        data = [q for q in data if q.get("concept") == concept]
    
    if not data: 
        return jsonify({"de": [], "message": "Không tìm thấy câu hỏi!"})

    so_luong_lay = min(so_cau, len(data))
    selected_qs = random.sample(data, so_luong_lay)
    
    de_sau_khi_tron = []
    for q in selected_qs:
        q_copy = q.copy()
        shuffled_options = list(q_copy["options"])
        random.shuffle(shuffled_options)
        q_copy["options"] = shuffled_options
        de_sau_khi_tron.append(q_copy)
    
    random.shuffle(de_sau_khi_tron)
    de_hien_tai = de_sau_khi_tron
    return jsonify({"de": de_hien_tai})

@app.route("/nop_bai", methods=["POST"])
def nop_bai():
    global de_hien_tai
    data = request.json
    student_name = data.get("student_name", "Ẩn danh")
    cau_tra_loi = data.get("cau_tra_loi", [])
    
    if not de_hien_tai:
        return jsonify({"error": "Chưa tạo đề"}), 400

    score, results, weak = 0, [], {}
    for q, ans in zip(de_hien_tai, cau_tra_loi):
        dung = (ans == q["answer"])
        if dung: score += 1
        else:
            c = q.get("concept", "unknown")
            weak[c] = weak.get(c, 0) + 1
            
        results.append({
            "cau_hoi": q["question"], 
            "tra_loi_cua_ban": ans, 
            "dap_an_dung": q["answer"], 
            "dung": dung
        })
    
    file_path = "lich_su_thi.csv"
    file_exists = os.path.isfile(file_path)
    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        with open(file_path, mode="a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Thời gian", "Thí sinh", "Số câu đúng", "Tổng số câu", "Phần trăm"])
            writer.writerow([thoi_gian, student_name, score, len(de_hien_tai), f"{round(score/len(de_hien_tai)*100, 2)}%"])
    except Exception as e:
        print("Lỗi lưu file CSV:", e)

    goi_y = [goi_y_hoc[k] for k in weak if k in goi_y_hoc]
    
    return jsonify({
        "diem": score, 
        "phan_tram": round(score/len(de_hien_tai)*100, 2), 
        "ket_qua": results, 
        "goi_y": goi_y
    })

@app.route("/chat_ai", methods=["POST"])
def chat_ai():
    data = request.json
    msg = data.get("message", "")
    user_name = data.get("user_name", "Học sinh")
    ctx = data.get("context")

    # Nếu có context chứa thông tin câu sai
    if ctx and "student_choice" in ctx:
        response = phan_tich_hoc_tap(ctx['student_choice'], user_name=user_name)
        return jsonify({"answer": response})

    # Chat bình thường
    response = hoi_ai(msg, user_name=user_name)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)