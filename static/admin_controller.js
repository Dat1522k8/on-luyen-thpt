/**
 * HỆ THỐNG QUẢN TRỊ VIÊN THPT VIỆT ĐỨC
 * File xử lý các tính năng: Import Word, Thêm câu hỏi, Xử lý ảnh (Paste/Upload), Xuất bản đề
 */

// --- HÀM TẠO HTML (SỬA ĐỂ NHẬN DIỆN CLICK/PASTE TỐT HƠN) ---
function generateCardHTML(index, content, opts = [], answer = "", explain = "", imgBase64 = null, type = "multiple_choice", sub_questions = []) {
    let inputZone = '';

    // DẠNG 1: TRẮC NGHIỆM 4 LỰA CHỌN
    if (type === 'multiple_choice') {
        inputZone = `
            <div class="opt-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                ${[0, 1, 2, 3].map(i => `
                    <input type="text" class="opt-val" value="${opts[i] || ''}" placeholder="Đáp án ${String.fromCharCode(65 + i)}">
                `).join('')}
            </div>
            <div style="margin-top:15px;">
                <label><strong>Đáp án đúng:</strong> 
                    <select class="q-ans-select">
                        ${['A', 'B', 'C', 'D'].map(char => `<option value="${char}" ${answer === char ? 'selected' : ''}>${char}</option>`).join('')}
                    </select>
                </label>
            </div>`;
    } 
    // DẠNG 2: TRẮC NGHIỆM ĐÚNG SAI
    else if (type === 'true_false') {
        inputZone = `
            <div class="tf-edit-zone" style="margin-top:10px; background: #f9f9f9; padding: 10px; border-radius: 8px;">
                <p style="font-size: 0.8rem; color: #666; margin-bottom: 8px;">Nhập nội dung các khẳng định a, b, c, d:</p>
                ${[0, 1, 2, 3].map(i => {
                    const sub = sub_questions[i] || { text: "", answer: "Đ" };
                    return `
                    <div style="display:flex; gap:10px; margin-bottom:8px; align-items: center;">
                        <span style="font-weight:bold;">${String.fromCharCode(97 + i)})</span>
                        <input type="text" class="tf-sub-text" style="flex:1; padding: 5px;" value="${sub.text}" placeholder="Nội dung khẳng định...">
                        <select class="tf-sub-ans" style="padding: 5px;">
                            <option value="Đ" ${sub.answer === 'Đ' ? 'selected' : ''}>Đúng</option>
                            <option value="S" ${sub.answer === 'S' ? 'selected' : ''}>Sai</option>
                        </select>
                    </div>`;
                }).join('')}
            </div>`;
    } 
    // DẠNG 3: TRẢ LỜI NGẮN
    else if (type === 'short_answer') {
        inputZone = `
            <div style="margin-top:15px; background: #fff5eb; padding: 15px; border-radius: 8px; border: 1px dashed #ff7a18;">
                <strong>Đáp số chính xác:</strong>
                <input type="text" class="short-ans-val" value="${answer}" placeholder="Nhập số hoặc từ khóa (VD: 27 hoặc 5.5)" 
                       style="width:100%; padding:10px; margin-top:5px; border:1px solid #ddd; border-radius:5px;">
            </div>`;
    }

    return `
        <div class="edit-q-card" data-type="${type}" data-image-base64="${imgBase64 || ''}" 
             style="background: white; border: 1px solid #ddd; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="background:#ff7a18; color:white; padding:3px 10px; border-radius:15px; font-size:12px; font-weight:bold;">
                    ${type === 'multiple_choice' ? 'TRẮC NGHIỆM' : (type === 'true_false' ? 'ĐÚNG / SAI' : 'TRẢ LỜI NGẮN')}
                </span>
                <button style="background:none; color:#ff4757; border:none; cursor:pointer; font-weight:bold;" onclick="this.closest('.edit-q-card').remove()">
                    <i class="fas fa-trash"></i> Xóa câu này
                </button>
            </div>

            <textarea rows="3" class="q-content-input" style="width:100%; padding:10px; border:1px solid #eee; border-radius:8px; font-family:inherit;" placeholder="Nội dung câu hỏi...">${content}</textarea>
            
            <div class="image-attach-zone" tabindex="0" onpaste="handlePaste(event, this)" onclick="this.querySelector('input').click()"
                 style="cursor: pointer; border: 2px dashed #eee; padding: 10px; text-align: center; margin: 10px 0; border-radius: 8px;">
                <div class="preview-img-slot">
                    ${imgBase64 ? `<img src="${imgBase64}" style="max-width:200px; border-radius:5px;">` : '<i class="fas fa-image" style="color: #ccc;"></i> <small>Dán ảnh hoặc Click để chọn file</small>'}
                </div>
                <input type="file" accept="image/*" style="display:none" onchange="previewImage(this)">
            </div>

            ${inputZone}

            <textarea rows="2" class="q-explain-input" style="width:100%; margin-top:10px; padding:8px; border:1px solid #f0f0f0; border-radius:5px; font-size:0.9rem;" placeholder="Lời giải chi tiết (không bắt buộc)...">${explain || ""}</textarea>
        </div>
    `;
}

// --- LOGIC XỬ LÝ ẢNH (DÙNG CƠ CHẾ TÌM THẺ CHA - KHÔNG DÙNG INDEX) ---

function handlePaste(event, zoneElement) {
    const items = (event.clipboardData || event.originalEvent.clipboardData).items;
    for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf("image") !== -1) {
            const blob = items[i].getAsFile();
            const reader = new FileReader();
            reader.onload = function(e) {
                updateImageInCard(zoneElement, e.target.result);
            };
            reader.readAsDataURL(blob);
        }
    }
}
function previewImage(inputElement) {
    if (inputElement.files && inputElement.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            updateImageInCard(inputElement.parentElement, e.target.result);
        };
        reader.readAsDataURL(inputElement.files[0]);
    }
}
function updateImageInCard(zoneElement, base64Data) {
    const slot = zoneElement.querySelector('.preview-img-slot');
    slot.innerHTML = `<img src="${base64Data}" style="max-width:100%; max-height:200px; border-radius:5px;">`;
    const card = zoneElement.closest('.edit-q-card');
    card.setAttribute('data-image-base64', base64Data);
}

// --- CÁC HÀM CÒN LẠI (GIỮ NGUYÊN HOẶC CẬP NHẬT NHẸ) ---

document.getElementById('fileInput').onchange = async function(e) {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    const uploadZone = document.querySelector('.upload-zone');
    const oldHTML = uploadZone.innerHTML;
    uploadZone.innerHTML = `<i class="fas fa-spinner fa-spin" style="font-size:3rem; color:#ff7a18;"></i><p>Đang phân tích cấu trúc đề...</p>`;

    try {
        const response = await fetch('/api/admin/import-word', { method: 'POST', body: formData });
        const res = await response.json();
        if (res.status === 'success') {
            document.getElementById('step-1').style.display = 'none';
            document.getElementById('step-2').style.display = 'block';
            renderEditCards(res.questions);
        } else {
            alert("Lỗi: " + res.message);
            uploadZone.innerHTML = oldHTML;
        }
    } catch (err) { 
        alert("Lỗi kết nối Server!"); 
        location.reload(); 
    }
};

function renderEditCards(data) {
    const list = document.getElementById('questions-edit-list');
    list.innerHTML = data.map((item, index) => 
        generateCardHTML(
            index, 
            item.content, 
            item.options || [], 
            item.answer || "", 
            item.explanation || "", 
            item.image || null,
            item.type || "multiple_choice",
            item.sub_questions || []
        )
    ).join('');
    if (window.MathJax) MathJax.typesetPromise();
}
function addNewQuestion(type = 'multiple_choice') {
    const list = document.getElementById('questions-edit-list');
    const html = generateCardHTML(0, "", ["", "", "", ""], "A", "", null, type, []);
    list.insertAdjacentHTML('beforeend', html);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

async function publishQuiz() {
    const quizCode = document.getElementById('final-quiz-code').value;
    const duration = document.getElementById('time-val').innerText;
    if(!quizCode) return alert("Vui lòng nhập Mã đề thi!");

    const cards = document.querySelectorAll('.edit-q-card');
    const questions = Array.from(cards).map(card => {
        const type = card.getAttribute('data-type');
        let item = {
            type: type,
            content: card.querySelector('.q-content-input').value,
            explanation: card.querySelector('.q-explain-input').value,
            image: card.getAttribute('data-image-base64') || null
        };

        if (type === 'multiple_choice') {
            item.options = Array.from(card.querySelectorAll('.opt-val')).map(input => input.value);
            item.answer = card.querySelector('.q-ans-select').value;
        } 
        else if (type === 'true_false') {
            item.sub_questions = Array.from(card.querySelectorAll('.tf-sub-text')).map((input, i) => ({
                text: input.value,
                answer: card.querySelectorAll('.tf-sub-ans')[i].value
            }));
            // Lưu chuỗi đáp án tổng hợp (VD: a-Đ, b-S, c-Đ, d-S)
            item.answer = item.sub_questions.map((s, i) => `${String.fromCharCode(97+i).toLowerCase()}-${s.answer}`).join(', ');
        } 
        else if (type === 'short_answer') {
            item.answer = card.querySelector('.short-ans-val').value;
        }

        return item;
    });

    const response = await fetch('/api/admin/save-quiz', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ quiz_code: quizCode, duration, questions })
    });

    if(response.ok) { 
        alert("Chúc mừng! Đề thi " + quizCode + " đã sẵn sàng."); 
        location.reload(); 
    } else {
        alert("Có lỗi khi lưu đề. Vui lòng kiểm tra lại.");
    }
}

function showQuizList() {
    const mainArea = document.getElementById('step-1');
    const editArea = document.getElementById('step-2');
    
    // Hiện vùng step-1 để chứa danh sách
    mainArea.style.display = 'block';
    editArea.style.display = 'none';

    mainArea.innerHTML = `<h3><i class="fas fa-spinner fa-spin"></i> Đang tải kho đề...</h3>`;

    fetch('/api/admin/list-quizzes')
    .then(res => res.json())
    .then(data => {
        if (data.length === 0) {
            mainArea.innerHTML = `
                <h3>Kho đề đang trống</h3>
                <button onclick="location.reload()" class="btn-chat-free">Quay lại</button>
            `;
            return;
        }

        let listHtml = data.map(name => `
            <div style="padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background: white; margin-bottom: 5px; border-radius: 8px;">
                <span><i class="fas fa-file-alt" style="color: #ff7a18;"></i> <strong>${name}</strong></span>
                <div>
                    <button class="btn-chat-free" style="padding: 5px 12px;" onclick="window.open('/api/get-quiz?code=${name}', '_blank')">Xem File</button>
                </div>
            </div>
        `).join('');

        mainArea.innerHTML = `
            <div style="background: #f9f9f9; padding: 20px; border-radius: 15px;">
                <h2 style="color: #ff7a18;"><i class="fas fa-archive"></i> Kho đề thi đã lưu</h2>
                <div style="margin-bottom: 20px;">${listHtml}</div>
                <button onclick="location.reload()" class="btn-chat-free" style="width: 100%;">Quay lại tạo đề mới</button>
            </div>
        `;
    })
    .catch(err => {
        alert("Không thể kết nối server!");
        location.reload();
    });
}
// --- XEM DANH SÁCH BẢNG ĐIỂM ---
function showResultsList() {
    const mainArea = document.getElementById('step-1');
    document.getElementById('step-2').style.display = 'none';
    mainArea.style.display = 'block';

    mainArea.innerHTML = `<h3><i class="fas fa-chart-line"></i> Đang tải danh sách điểm...</h3>`;

    fetch('/api/admin/list-results')
    .then(res => res.json())
    .then(files => {
        if (files.length === 0) {
            mainArea.innerHTML = `<h3>Chưa có dữ liệu điểm.</h3><button onclick="location.reload()" class="btn-chat-free">Quay lại</button>`;
            return;
        }

        let html = `
            <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h2 style="color: #27ae60;"><i class="fas fa-poll"></i> Kết quả thi các lớp</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top: 20px;">
                    ${files.map(f => `
                        <div class="result-card" onclick="viewDetailResult('${f}')" 
                             style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; cursor: pointer; text-align: center; transition: 0.3s;">
                            <i class="fas fa-file-csv" style="font-size: 2rem; color: #27ae60;"></i>
                            <p style="margin-top: 10px; font-weight: bold;">${f.replace('.csv','')}</p>
                        </div>
                    `).join('')}
                </div>
                <button onclick="location.reload()" class="btn-chat-free" style="width: 100%; margin-top: 20px;">Quay lại</button>
            </div>
        `;
        mainArea.innerHTML = html;
    });
}

// --- XEM CHI TIẾT ĐIỂM TRONG 1 FILE ---
function viewDetailResult(filename) {
    const mainArea = document.getElementById('step-1');
    mainArea.innerHTML = `<h3>Đang đọc dữ liệu ${filename}...</h3>`;

    fetch(`/api/admin/get-result-detail?file=${filename}`)
    .then(res => res.json())
    .then(data => {
        let rowsHtml = data.map(row => `
            <tr>
                ${row.map(cell => `<td style="padding: 10px; border-bottom: 1px solid #eee;">${cell}</td>`).join('')}
            </tr>
        `).join('');

        mainArea.innerHTML = `
            <div style="background: white; padding: 20px; border-radius: 15px;">
                <h3 style="color: #27ae60;">Chi tiết kết quả: ${filename}</h3>
                <div style="overflow-x: auto; margin-top: 15px;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="background: #f8f9fa;">
                                <th style="padding: 10px;">Thời gian</th><th style="padding: 10px;">Học sinh</th>
                                <th style="padding: 10px;">Lớp</th><th style="padding: 10px;">Điểm</th>
                                <th style="padding: 10px;">Chi tiết</th>
                            </tr>
                        </thead>
                        <tbody>${rowsHtml}</tbody>
                    </table>
                </div>
                <div style="margin-top: 20px; display: flex; gap: 10px;">
                    <button onclick="showResultsList()" class="btn-chat-free">Quay lại danh sách</button>
                    <button onclick="window.open('/api/admin/download-result/${filename}')" class="btn-chat-free" style="background: #27ae60;">Tải về máy (.CSV)</button>
                </div>
            </div>
        `;
    });
}