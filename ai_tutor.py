import requests
import re

# Bộ nhớ đệm để lưu nội dung đề bài
BO_NHO_DE_BAI = {}

def hoi_ai(message, user_name="Học sinh", mode="tutor"):
    global BO_NHO_DE_BAI
    
    # CHỈ TỰ LẤY ĐỀ KHI ĐANG Ở CHẾ ĐỘ GIẢI BÀI (TUTOR)
    if mode == "tutor":
        match = re.search(r"(?:Câu|câu|cau)\s*(\d+)", message)
        if match:
            so_cau = match.group(1)
            key_cau = f"Câu {so_cau}"
            if key_cau in BO_NHO_DE_BAI:
                noi_dung_de = BO_NHO_DE_BAI[key_cau]
                message = f"Giải chi tiết giúp mình câu này:\n{noi_dung_de}\n(Lưu ý: Giải thích theo phong cách gia sư Cheems cho {user_name})"

    # ... (giữ nguyên phần gọi API phía dưới) ...
    # --- CẤU HÌNH API GROQ ---
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # --- NHẬP API KEY TRỰC TIẾP TẠI ĐÂY ---
    api_key = os.getenv("AI_API_KEY")
 # Thay toàn bộ chuỗi này bằng mã API thực tế của bạn
    
    if not api_key or api_key.startswith("gsk_xxxx"):
        return f"Lỗi: Đạt ơi, bạn chưa dán mã API Key thật vào code kìa!"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        f"Bạn là gia sư Cheems lầy lội, gọi người dùng là {user_name}. "
        "Khi giải bài: Tóm tắt -> Lời giải -> Công thức (LaTeX) -> Kết luận."
    )
    
    if mode == "summary":
        system_prompt = (
            f"Bạn là gia sư Cheems. Hãy liệt kê danh sách câu sai cho {user_name} "
            "và hỏi xem Đạt muốn thầy hướng dẫn giải chi tiết câu nào không."
        )
    else:
        system_prompt = (
            f"Bạn là thầy giáo Cheems, giảng bài theo chương trình GDPT của Việt Nam. "
            f"Đang hướng dẫn học sinh {user_name}. "
            "Khi giải bài, phải tuân thủ cấu trúc: "
            "1. Phương pháp: Nhắc lại công thức hoặc lý thuyết trọng tâm (SGK). "
            "2. Chi tiết: Các bước biến đổi toán học rõ ràng, dùng LaTeX. "
            "3. Chốt lại: Đáp án cuối cùng và lưu ý lỗi sai thường gặp (bẫy đề bài). "
            "Cách xưng hô: Thầy - em hoặc thầy - {user_name}. Ngôn ngữ sư phạm, dễ hiểu nhưng vẫn có nét lầy của Cheems."
        )
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
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Lỗi kết nối rồi {user_name} ơi! (Chi tiết: {str(e)})"

# --- CÁC HÀM PHỤ TRỢ ---
def phan_tich_hoc_tap(danh_sach_cau_sai, user_name="Học sinh"):
    # danh_sach_cau_sai là chuỗi số câu, ví dụ: "1, 3"
    prompt = (
        f"Thông báo cho {user_name} rằng họ đã làm sai các câu sau: Câu {danh_sach_cau_sai}. "
        "Yêu cầu: Chỉ liệt kê số câu và hỏi họ muốn giải chi tiết câu nào không. "
        "TUYỆT ĐỐI KHÔNG giải bài ở bước này."
    )
    return hoi_ai(prompt, user_name=user_name, mode="summary")

def cap_nhat_bo_nho_de(de_hien_tai):
    global BO_NHO_DE_BAI
    BO_NHO_DE_BAI.clear()
    for i, q in enumerate(de_hien_tai):
        BO_NHO_DE_BAI[f"Câu {i+1}"] = f"Câu hỏi: {q['question']}\nĐáp án đúng: {q['answer']}"