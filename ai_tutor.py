import requests
import os

# Lấy API Key từ biến môi trường của hệ thống
API_KEY = os.getenv("GROQ_API_KEY", "") 

def hoi_ai(message):
    if not API_KEY:
        return "Lỗi: Chưa cấu hình API Key trên server."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    # ... giữ nguyên phần còn lại ...

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [

        {
        "role": "system",
        "content": "Bạn là gia sư Toán và Vật lý. Giải thích dễ hiểu bằng tiếng Việt. Viết công thức bằng LaTeX."
        },

        {
        "role": "user",
        "content": message
        }

        ]
    }

    try:

        r = requests.post(url, headers=headers, json=data, timeout=30)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            print("AI API ERROR:", r.text)
            return "AI đang lỗi API."

        result = r.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        print("AI ERROR:", e)

        return "AI đang gặp lỗi."

# =====================
# PHÂN TÍCH BÀI LÀM
# =====================

def phan_tich_hoc_tap(cau_sai):

    if len(cau_sai) == 0:
        return "Bạn làm rất tốt, không có câu sai."

    prompt = f"""
Học sinh làm sai các câu sau:

{cau_sai}

Hãy:
1. Phân tích học sinh yếu phần kiến thức nào
2. Gợi ý cách học lại
3. Đưa lộ trình ôn tập
"""

    return hoi_ai(prompt)