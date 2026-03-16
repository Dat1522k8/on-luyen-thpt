import requests
import os

# Lấy API Key từ biến môi trường
API_KEY = os.getenv("AI_API_KEY", "") 

def hoi_ai(message):
    if not API_KEY:
        return "Lỗi: Chưa cấu hình API Key trên server."
    
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # PROMPT HỆ THỐNG: "Trái tim" để AI hiểu văn hóa giáo dục Việt Nam
    system_instruction = (
        "Bạn là một gia sư Toán và Vật lý chuyên nghiệp tại Việt Nam. "
        "Hãy tuân thủ các quy tắc sau:\n"
        "1. Ngôn ngữ: Dùng văn phong sư phạm Việt Nam, xưng hô 'Thầy/Cô' và 'Em' hoặc 'Bạn'.\n"
        "2. Định dạng số: Sử dụng dấu phẩy (,) cho phần thập phân (ví dụ: 9,5 thay vì 9.5).\n"
        "3. Ký hiệu: Sử dụng ký hiệu Toán/Lý theo chuẩn Sách giáo khoa mới của Bộ Giáo dục Việt Nam. "
        "Ví dụ: dùng sin, cos, tan, cot; đơn vị đo lường dùng km/h, m/s^2...\n"
        "4. Trình bày: Viết công thức bằng LaTeX (ví dụ: $x = \\frac{-b}{2a}$). "
        "Giải thích từng bước rõ ràng, không nhảy bước quá nhanh.\n"
        "5. Nội dung: Nếu giải bài tập, phải có các bước: Tóm tắt - Lời giải - Công thức áp dụng - Kết luận."
    )

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7  # Giúp câu trả lời mềm mại, tự nhiên hơn
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if r.status_code != 200:
            return f"AI đang lỗi API (Status: {r.status_code})."

        result = r.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI ERROR:", e)
        return "AI đang gặp sự cố kết nối."

# =====================
# PHÂN TÍCH BÀI LÀM
# =====================

def phan_tich_hoc_tap(cau_sai):
    if not cau_sai:
        return "Chúc mừng! Bạn đã hoàn thành xuất sắc bài tập mà không sai câu nào. Hãy tiếp tục phát huy nhé!"

    # Prompt này giúp AI đóng vai người tư vấn học tập tại Việt Nam
    prompt = f"""
Học sinh làm sai các câu sau:
{cau_sai}

Hãy thực hiện:
1. Nhận xét cụ thể học sinh đang hổng kiến thức ở chủ đề nào (Dựa theo chương trình GDPT Việt Nam).
2. Giải thích ngắn gọn lỗi sai thường gặp ở các câu này.
3. Đưa ra lời khuyên về tài liệu hoặc phương pháp ôn tập (ví dụ: làm thêm bài tập trong SBT, xem lại định nghĩa...).
4. Đưa ra một lộ trình học tập 3 bước để khắc phục.
"""
    return hoi_ai(prompt)