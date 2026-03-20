import requests
import re
import os  # Thư viện để làm việc với hệ thống

# Bộ nhớ đệm để lưu nội dung đề bài
BO_NHO_DE_BAI = {}

def hoi_ai(message, user_name="Học sinh", mode="tutor"):
    global BO_NHO_DE_BAI
    
    # --- LOGIC TỰ ĐỘNG LẤY ĐỀ BÀI TỪ BỘ NHỚ ---
    match = re.search(r"(?:Câu|câu|cau)\s*(\d+)", message)
    if match:
        so_cau = match.group(1)
        key_cau = f"Câu {so_cau}"
        if key_cau in BO_NHO_DE_BAI:
            noi_dung_de = BO_NHO_DE_BAI[key_cau]
            message = f"Giải chi tiết giúp mình câu này:\n{noi_dung_de}\n(Lưu ý: Giải thích theo phong cách gia sư Cheems cho {user_name})"

    # --- CẤU HÌNH API GROQ ---
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Lấy API Key từ biến môi trường của Render
    # Nếu chạy local mà chưa có biến môi trường, nó sẽ trả về None hoặc chuỗi rỗng
    api_key = os.getenv("AI_API_KEY")
    
    if not api_key:
        return f"Lỗi: Chưa cấu hình GROQ_API_KEY trên hệ thống rồi {user_name} ơi!"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        f"Bạn là gia sư Cheems lầy lội, gọi người dùng là {user_name}. "
        "Khi giải bài: Tóm tắt -> Lời giải -> Công thức (LaTeX) -> Kết luận."
    )
    
    if mode == "summary":
        system_prompt = f"Bạn là Cheems. Hãy liệt kê danh sách câu sai cho {user_name} một cách ngắn gọn và bảo họ chọn câu để sửa."

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status() # Kiểm tra lỗi HTTP (4xx, 5xx)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Lỗi kết nối rồi {user_name} ơi! (Chi tiết: {str(e)})"

# --- CÁC HÀM PHỤ TRỢ (GIỮ NGUYÊN) ---
def phan_tich_hoc_tap(du_lieu_raw, user_name="Học sinh"):
    content = str(du_lieu_raw)
    so_cau_sai = re.findall(r"Câu\s*(\d+)", content)
    if not so_cau_sai:
        so_cau_sai = re.findall(r"(\d+)", content)
    if not so_cau_sai:
        return f"Chào {user_name}, mình chưa thấy danh sách câu sai nào cả!"
    ds_hien_thi = [f"Câu {n}" for n in so_cau_sai]
    prompt = f"Dưới đây là danh sách các câu mà {user_name} làm sai: {', '.join(ds_hien_thi)}. Hãy liệt kê lại và hỏi họ muốn sửa câu nào."
    return hoi_ai(prompt, user_name=user_name, mode="summary")

def cap_nhat_bo_nho_de(de_hien_tai):
    global BO_NHO_DE_BAI
    BO_NHO_DE_BAI.clear()
    for i, q in enumerate(de_hien_tai):
        BO_NHO_DE_BAI[f"Câu {i+1}"] = f"Câu hỏi: {q['question']}\nĐáp án đúng: {q['answer']}"