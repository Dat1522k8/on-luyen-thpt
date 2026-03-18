from flask import Flask, render_template, jsonify, request
import json
import random
import os

app = Flask(__name__)

# Lưu trữ đề hiện tại để đối chiếu khi nộp bài
de_hien_tai = []

# SỬA LỖI: Cập nhật key gợi ý khớp hoàn toàn với Concept tiếng Việt trong JSON để nop_bai hoạt động
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
        # SỬA LỖI: Kiểm tra file tồn tại trước khi mở để tránh lỗi crash
        if not os.path.exists(filename):
            print(f"Cảnh báo: Không tìm thấy file {filename}")
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
        concepts = ["hàm số và đồ thị", "nguyên hàm tích phân", "hình học không gian", "khối tròn xoay", "tọa độ không gian", "số mũ và logarit", "số phức", "tổ hợp và xác suất",
"đạo hàm", "cấp số cộng", "cấp số nhân", "tiệm cận"]
    else:
        # SỬA LỖI: Danh sách này phải khớp 100% với trường "concept" trong file physics.json
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
        # SỬA LỖI: Đảm bảo so sánh chuỗi chính xác để lọc được dữ liệu vật lý
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
    data = request.json
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
    
    # SỬA LỖI: Lấy gợi ý dựa trên các concept bị sai
    goi_y = [goi_y_hoc[k] for k in weak if k in goi_y_hoc]
    
    return jsonify({
        "diem": score, 
        "phan_tram": round(score/len(de_hien_tai)*100, 2), 
        "ket_qua": results, 
        "goi_y": goi_y
    })

# Các route còn lại (ai_lo_trinh, chat_ai) giữ nguyên như cũ
@app.route("/ai_lo_trinh", methods=["POST"])
def ai_lo_trinh():
    from ai_tutor import phan_tich_hoc_tap
    data = request.json
    cau_sai = data.get("cau_sai", [])
    result = phan_tich_hoc_tap(cau_sai)
    return jsonify({"answer": result})

@app.route("/chat_ai", methods=["POST"])
def chat_ai():
    from ai_tutor import hoi_ai
    data = request.json
    msg = data.get("message", "")
    ctx = data.get("context")
    if ctx:
        prompt = f"Câu hỏi: {ctx['question']}\nĐúng: {ctx['correct_answer']}\nHọc sinh chọn: {ctx['student_choice']}\nCâu hỏi: {msg}"
    else:
        prompt = msg
    return jsonify({"answer": hoi_ai(prompt)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)