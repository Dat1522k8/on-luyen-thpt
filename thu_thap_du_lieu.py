import json
import os
import requests
import re
import time

# ==========================================
# CẤU HÌNH GROQ API
# ==========================================
GROQ_API_KEY = "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"
MODEL_NAME = "llama-3.3-70b-versatile"
DATA_FOLDER = "dataset"

def fetch_from_ai(subject_name, concept_display, concept_slug, level, quantity):
    """Gọi API và ép AI nhả đúng nội dung đáp án"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Tạo {quantity} câu hỏi trắc nghiệm {subject_name}. Chủ đề: {concept_display}. Mức độ: {level}.
    
    YÊU CẦU QUAN TRỌNG:
    1. Trường 'options' PHẢI chứa nội dung chi tiết (số hoặc biểu thức LaTeX), KHÔNG được ghi "A", "B", "C", "D".
    2. Trường 'answer' PHẢI là nội dung của đáp án đúng (phải khớp 100% với 1 trong 4 options).
    3. Cấu trúc JSON:
    {{
        "level": "{level}",
        "question": "Nội dung câu hỏi...",
        "options": ["Nội dung 1", "Nội dung 2", "Nội dung 3", "Nội dung 4"],
        "answer": "Nội dung đúng",
        "concept": "{concept_slug}"
    }}
    Lưu ý: Dùng \\\\ cho LaTeX. Trả về DUY NHẤT mảng JSON.
    """

    payload = { # Đã đổi tên thành payload để tránh nhầm lẫn
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a professional teacher. Output ONLY a clean JSON array. No conversational text."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code != 200: 
            print(f"      ❌ API Error: {response.status_code}")
            return []
        
        content = response.json()["choices"][0]["message"]["content"].strip()
        # Làm sạch JSON
        content = re.sub(r'```json|```', '', content).strip()
        content = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', content)
        
        return json.loads(content)
    except Exception as e:
        print(f"      ⚠️ Lỗi xử lý: {e}")
        return []

def fetch_and_append(subject_name, concept_display, concept_slug, level, total_qty, filename):
    print(f"🚀 [{subject_name}] Thu thập {total_qty} câu: {concept_display}")
    
    batch_size = 2 # Chia nhỏ 5 câu/lần để AI làm kỹ nhất
    all_valid_qs = []
    
    for i in range(0, total_qty, batch_size):
        current_qty = min(batch_size, total_qty - i)
        print(f"   -> Đang lấy nhóm {i+1}...")
        
        res = fetch_from_ai(subject_name, concept_display, concept_slug, level, current_qty)
        
        if isinstance(res, list):
            valid_batch = [q for q in res if q.get('answer') in q.get('options', [])]
            all_valid_qs.extend(valid_batch)
        
        time.sleep(1.5) # Nghỉ để tránh Rate Limit

    if all_valid_qs:
        if not os.path.exists(DATA_FOLDER): os.makedirs(DATA_FOLDER)
        path = os.path.join(DATA_FOLDER, filename)
        
        existing_data = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: existing_data = json.load(f)
                except: existing_data = []

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing_data + all_valid_qs, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Xong: Đã lưu thêm {len(all_valid_qs)} câu vào {filename}.")

# ==========================================
# CHẠY THỬ NGHIỆM
# ==========================================
if __name__ == "__main__":
    # Thử nghiệm mỗi môn 10 câu (chia làm 2 đợt)

    #TOÁN
    #fetch_and_append("Toán", "Đạo hàm", "dao_ham", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "nguyên hàm", "nguyen_ham", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "logarit", "logarit", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "cấp số cộng", "cap_so_cong", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "cấp số nhân", "cap_so_nhan", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "nhân xác suất", "nha_xac_xuat", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "xác xuất", "xac_suat", "Khó", 10, "math.json")
    #fetch_and_append("Toán", "xác xuất có điều kiện", "xac_suat_co_dieu_kien", "Khó", 10, "math.json")
    #LÝ
    fetch_and_append("Vật lý", "Từ trường", "tu_truong", "Khó", 20, "physics.json")
    fetch_and_append("Vật lý", "điện áp", "dien_ap", "Khó", 20, "physics.json")
    fetch_and_append("Vật lý", "khí lý tưởng", "khi_ly_tuong", "Khó", 20, "physics.json")
    fetch_and_append("Vật lý", "hạt nhân", "hat_nhan", "Khó", 20, "physics.json")
    fetch_and_append("Vật lý", "mô men lực", "mo_men_luc", "Khó", 20, "physics.json")
    fetch_and_append("Vật lý", "phương trình trạng thái", "pttt", "Khó", 20, "physics.json")
    fetch_and_append("Vật lý", "vật lý nhiệt", "vat_ly_nhiet", "Khó", 20, "physics.json")