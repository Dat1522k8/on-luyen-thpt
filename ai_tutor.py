import requests
import re
import os

# Bộ nhớ đệm để lưu nội dung đề bài
BO_NHO_DE_BAI = {}

def hoi_ai(message, user_name="Học sinh", mode="tutor"):
    global BO_NHO_DE_BAI
    
    # --- 1. CHỈ TỰ LẤY ĐỀ KHI KHÔNG PHẢI CHẾ ĐỘ CHỜ ---
    if mode == "tutor" and "[WAIT_MODE]" not in message:
        match = re.search(r"(?:Câu|câu|cau)\s*(\d+)", message)
        if match:
            so_cau = match.group(1)
            key_cau = f"Câu {so_cau}"
            if key_cau in BO_NHO_DE_BAI:
                noi_dung_de = BO_NHO_DE_BAI[key_cau]
                message = f"Giải chi tiết giúp mình câu này:\n{noi_dung_de}\n(Lưu ý: Giải thích theo phong cách gia sư Cheems cho {user_name})"

    # --- 2. THIẾT LẬP SYSTEM PROMPT DUY NHẤT ---
    # Không dùng if mode nữa mà lồng vào trong một khối thống nhất
    if "[WAIT_MODE]" in message:
        system_prompt = (
            f"Mày là Gia sư Cheems lầy lội tại Việt Đức. Đang dạy bro {user_name}. "
            f"NHIỆM VỤ: Chào hỏi lầy lội và liệt kê các số câu sai. "
            f"TUYỆT ĐỐI CẤM GIẢI BÀI, CẤM đưa ra phương pháp hay đáp án lúc này. "
            f"Chốt hạ bằng câu hỏi: 'Bro {user_name} muốn Cheems nấu câu nào trước?'"
        )
    else:
        # Chế độ giải bài (Tutor)
        system_prompt = f"""
        Mày là "Gia sư Cheems" - Huyền thoại Toán Lý tại Việt Đức. Đang dạy bro {user_name}.
        Phong cách: Lầy lội, Gen Z (bro, đỉnh nóc, kịch trần, khum, chê).
        
        QUY TẮC GIẢI BÀI:
        1. Phương pháp: Nhắc công thức $...$
        2. Chi tiết: Biến đổi $$...$$
        3. Chốt lại: Đáp án và bẫy đề bài.
        
        LƯU Ý: Luôn dùng LaTeX $ cho nội dòng và $$ cho xuống dòng. KHÔNG dùng \[ \] hay \( \).
        """

    # --- 3. CẤU HÌNH API GROQ ---
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.getenv("AI_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

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
        response.raise_for_status() 
        answer = response.json()["choices"][0]["message"]["content"]
        
        # --- 4. FIX LATEX HIỂN THỊ ---
        answer = answer.replace("\\[", "$$").replace("\\]", "$$")
        answer = answer.replace("\\(", "$").replace("\\)", "$")
        return answer
        
    except Exception as e:
        return f"Lỗi kết nối rồi {user_name} ơi! (Chi tiết: {str(e)})"

# --- GIỮ NGUYÊN CÁC HÀM PHỤ TRỢ DƯỚI ĐÂY ---
def phan_tich_hoc_tap(danh_sach_cau_sai, user_name="Học sinh"):
    # Truyền thêm [WAIT_MODE] để kích hoạt chặn giải bài
    prompt = f"[WAIT_MODE] Hệ thống: Học sinh đã làm sai các câu sau: Câu {danh_sach_cau_sai}."
    return hoi_ai(prompt, user_name=user_name, mode="tutor")

def cap_nhat_bo_nho_de(de_hien_tai):
    global BO_NHO_DE_BAI
    BO_NHO_DE_BAI.clear()
    for i, q in enumerate(de_hien_tai):
        BO_NHO_DE_BAI[f"Câu {i+1}"] = f"Câu hỏi: {q['question']}\nĐáp án đúng: {q['answer']}"