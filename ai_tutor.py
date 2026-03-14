import requests

API_KEY = "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"

# =====================
# CHAT AI
# =====================

def hoi_ai(message):

    url = "https://api.groq.com/openai/v1/chat/completions"

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