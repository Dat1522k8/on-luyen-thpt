// BIẾN TOÀN CỤC
let danh_sach_cau_hoi = [];
let cau_sai_list = [];
let timerInterval;

// --- 1. HÀM ĐĂNG NHẬP ---
//
// --- 2. LOGIC TẢI ĐỀ ---
function taiConcept() {
    let mon = document.getElementById("mon").value;
    fetch("/concepts?mon=" + mon)
        .then(res => res.json())
        .then(data => {
            let select = document.getElementById("concept");
            if(!select) return;
            select.innerHTML = '<option value="all">Tất cả chủ đề</option>';
            data.forEach(c => { select.innerHTML += `<option value="${c}">${c}</option>`; });
        });
}

function taiDe() {
    let mon = document.getElementById("mon").value;
    let concept = document.getElementById("concept").value;
    let so_cau = document.getElementById("so_cau").value;
    
    fetch(`/tao_de?mon=${mon}&concept=${concept}&so_cau=${so_cau}`)
    .then(res => res.json())
    .then(data => {
        danh_sach_cau_hoi = data.de || [];
        let html = "";
        danh_sach_cau_hoi.forEach((q, i) => {
            html += `
            <div class="question-card">
                <h3>Câu ${i+1}</h3>
                <div class="question-text">${q.question}</div>
                <div class="options-container">
                    ${q.options.map(opt => `
                        <label class="option">
                            <input type="radio" name="cau${i}" value="${opt}"> 
                            <span>${opt}</span>
                        </label>
                    `).join('')}
                </div>
            </div>`;
        });
        document.getElementById("de").innerHTML = html;
        document.getElementById("ketqua").innerHTML = "";
        document.getElementById("btn-analyze").style.display = "none";
        
        if (window.MathJax) MathJax.typesetPromise();
        batDauDemNguoc();
    });
}

// --- 3. THỜI GIAN & NỘP BÀI ---
function batDauDemNguoc() {
    clearInterval(timerInterval);
    let timeLeft = (parseInt(document.getElementById("so_cau").value) || 5) * 120;
    const totalTime = timeLeft;
    const timerCont = document.getElementById("timer-container");
    timerCont.style.display = "block";

    timerInterval = setInterval(() => {
        let m = Math.floor(timeLeft / 60);
        let s = timeLeft % 60;
        document.getElementById("timer-display").innerText = `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
        document.getElementById("progress-fill").style.width = (timeLeft/totalTime)*100 + "%";
        if (timeLeft <= 0) { clearInterval(timerInterval); nopBai(); }
        timeLeft--;
    }, 1000);
}

function nopBai() {
    let studentFullName = (window.userName || "Thí sinh") + " - " + (window.userClass || "");
    let ans = [];
    
    for(let i=0; i<danh_sach_cau_hoi.length; i++) {
        let chk = document.querySelector(`input[name="cau${i}"]:checked`);
        if(!chk) { alert("Đạt ơi, bạn chưa làm hết bài kìa!"); return; }
        ans.push(chk.value);
    }
    
    clearInterval(timerInterval);
    document.getElementById("timer-container").style.display = "none";

    fetch("/nop_bai", { 
        method: "POST", 
        headers: {"Content-Type":"application/json"}, 
        body: JSON.stringify({ student_name: studentFullName, cau_tra_loi: ans }) 
    })
    .then(res => res.json()).then(data => {
        cau_sai_list = data.ket_qua.filter(k => !k.dung);
        const btnAnalyze = document.getElementById("btn-analyze");
        if(btnAnalyze) btnAnalyze.style.display = cau_sai_list.length > 0 ? "inline-block" : "none";

        let html = `<h2>Kết quả: ${studentFullName} - ${data.diem}/${danh_sach_cau_hoi.length}</h2>`;
        data.ket_qua.forEach((kq, i) => {
            let color = kq.dung ? "green" : "red";
            html += `<div class="question-card" style="border-left: 5px solid ${color}">
                <b>Câu ${i+1}:</b> ${kq.cau_hoi}<br>
                Chọn: <span style="color:${color}">${kq.tra_loi_cua_ban}</span> | Đáp án đúng: <b>${kq.dap_an_dung}</b>
            </div>`;
        });
        document.getElementById("ketqua").innerHTML = html;
        window.scrollTo(0, 0);
        if (window.MathJax) MathJax.typesetPromise();
        if (data.diem === danh_sach_cau_hoi.length && data.diem > 0) {
        setTimeout(() => {
            showSpecialCongrats(); // Gọi anh Bảnh lên quẩy
        }, 500);
    }
    });
}

// --- 4. GIAO DIỆN CHAT AI ---
function renderMessage(sender, text) {
    const chatbox = document.getElementById("chatbox");
    const isAI = sender === "ai";
    const displayName = isAI ? "Gia sư Cheems" : (window.userName || "Học sinh");
    const imgUrl = isAI ? "/static/cheems.jpg" : ""; 
    const msgRowClass = isAI ? "ai-msg-row" : "user-msg-row";
    const avatarHtml = isAI ? `<img src="${imgUrl}" class="chat-avt">` : "";

    const html = `
        <div class="msg-row ${msgRowClass}">
            ${avatarHtml}
            <div class="msg-content-wrapper">
                <div class="msg-bubble">${text}</div>
                <div class="msg-author">${displayName}</div>
            </div>
        </div>`;
    
    chatbox.innerHTML += html;
    chatbox.scrollTop = chatbox.scrollHeight;

    // QUAN TRỌNG: Lệnh này giúp MathJax quét lại toàn bộ chatbox để vẽ công thức
    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise([chatbox]).catch((err) => console.log("Lỗi MathJax:", err));
    }
}

function guiTinNhanAI() {
    const input = document.getElementById("ai_input");
    let userMsg = input.value.trim();
    if (!userMsg) return;

    renderMessage("user", userMsg);
    input.value = "";

    // TỰ ĐỘNG KIỂM TRA: Nếu học sinh hỏi "giải câu X"
    let match = userMsg.match(/giải câu (\d+)/i);
    let extraContext = "";

    if (match) {
        let soCau = parseInt(match[1]);
        // Tìm đề bài của câu đó trong danh sách câu hỏi gốc
        let cauHoiGoc = danh_sach_cau_hoi[soCau - 1]; 
        if (cauHoiGoc) {
            extraContext = `\n(Dữ liệu đề bài cho bạn giải: ${cauHoiGoc.question}. Đáp án đúng là: ${cauHoiGoc.answer})`;
        }
    }

    fetch("/chat_ai", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ 
            message: userMsg + extraContext, // Gộp đề bài vào đây khi học sinh hỏi
            user_name: window.userName || "ông bạn"
        })
    }).then(res => res.json()).then(data => {
        renderMessage("ai", data.answer);
    });
}

function phanTichAI() {
    console.log("Đang bắt đầu phân tích...");

    if (typeof cau_sai_list === 'undefined' || cau_sai_list.length === 0) {
        alert("Bạn chưa làm sai câu nào hoặc chưa nộp bài!");
        return;
    }
    
    const panel = document.getElementById("ai-panel");
    if (panel) panel.style.display = "flex";
    
    const tenHocSinh = window.userName || "ông bạn";

    // 1. Lấy danh sách số câu sai (Câu 1, Câu 2...)
    let danhSachSoCau = cau_sai_list.map(sai => {
        let index = danh_sach_cau_hoi.findIndex(q => q.question === sai.cau_hoi);
        return `Câu ${index + 1}`;
    }).join(", ");

    // 2. Tạo nội dung tin nhắn DUY NHẤT kèm Mật lệnh cấm giải
    const lenhGuiAI = `[WAIT_MODE] Hệ thống: Học sinh ${tenHocSinh} vừa làm sai các câu sau: ${danhSachSoCau}. 
    YÊU CẦU: Chỉ chào và liệt kê số câu sai. TUYỆT ĐỐI KHÔNG GIẢI BÀI LÚC NÀY.`;

    renderMessage("ai", `Đợi Cheems xíu, đang check list lỗi sai của bro ${tenHocSinh}...`);

    // 3. Chỉ Fetch 1 lần duy nhất
    fetch("/chat_ai", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ 
            message: lenhGuiAI, 
            user_name: tenHocSinh 
        })
    })
    .then(res => res.json())
    .then(data => {
        renderMessage("ai", data.answer);
    })
    .catch(err => {
        console.error("Lỗi:", err);
        renderMessage("ai", "Server lag rồi bro ơi!");
    });
}
// --- 5. TIỆN ÍCH ---
function toggleChat() {
    const panel = document.getElementById("ai-panel");
    if (panel.style.display === "flex") {
        panel.style.display = "none";
    } else {
        panel.style.display = "flex";
        // Khi mở chat thì cuộn xuống dưới cùng luôn cho tiện
        const chatbox = document.getElementById("chatbox");
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}
function moChatTuDo() {
    const panel = document.getElementById("ai-panel");
    panel.style.display = "flex"; // Hiện khung chat nổi lên
    
    // Cuộn xuống tin nhắn cuối cùng cho mượt
    const chatbox = document.getElementById("chatbox");
    if(chatbox) chatbox.scrollTop = chatbox.scrollHeight;
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("mon").addEventListener("change", taiConcept);
});
// --- LOGIC CHÚC MỪNG TÁCH NỀN KHÁ BẢNH ---

function startChromaKey() {
    const video = document.getElementById('raw-video');
    const canvas = document.getElementById('keyed-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    function render() {
        if (video.paused || video.ended) return;
        
        // Cập nhật kích thước canvas theo video
        if (canvas.width !== video.videoWidth) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        }

        ctx.drawImage(video, 0, 0);
        const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const length = frame.data.length;

        for (let i = 0; i < length; i += 4) {
            const r = frame.data[i];
            const g = frame.data[i + 1];
            const b = frame.data[i + 2];
            
            // Tách nền xanh lá: Nếu màu Green trội hơn Red và Blue
            if (g > 100 && g > r * 1.4 && g > b * 1.4) {
                frame.data[i + 3] = 0; // Độ trong suốt = 0
            }
        }
        ctx.putImageData(frame, 0, 0);
        requestAnimationFrame(render);
    }
    video.play().catch(e => console.log("Chưa chạy được video:", e));
    render();
}

function showFireWorks() {
    const box = document.getElementById('fireworks-box');
    box.innerHTML = ''; // Reset
    for (let i = 0; i < 60; i++) {
        const dot = document.createElement('div');
        dot.className = 'firework-dot';
        dot.style.left = Math.random() * 100 + '%';
        dot.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
        dot.style.animationDelay = Math.random() * 3 + 's';
        box.appendChild(dot);
    }
}

function showSpecialCongrats() {
    const name = window.userName || "Ái My";
    const nameElement = document.getElementById('congrats-name');
    if (nameElement) {
        nameElement.innerText = `CHÚC MỪNG ${name.toUpperCase()}!`;
    }
    
    const modal = document.getElementById('congrats-modal');
    const video = document.getElementById('raw-video');
    
    modal.style.display = 'block';

    // 1. Thiết lập âm thanh video (vặn volume to lên)
    video.muted = false; 
    video.volume = 1.0; 

    // 2. Tự động đóng khi hết video nhảy
    video.onended = function() {
        closeCongrats(); 
    };

    startChromaKey(); // Bắt đầu vẽ lên canvas (nhạc sẽ tự phát theo video.play())
    showFireWorks();  
}

function closeCongrats() {
    const modal = document.getElementById('congrats-modal');
    const video = document.getElementById('raw-video');

    modal.style.display = 'none';
    
    if (video) {
        video.pause();
        video.currentTime = 0; 
    }
    // Không cần xử lý 'win-audio' nữa vì đã dùng nhạc từ video
}
// 2. Logic kéo thả bong bóng (Drag & Drop)
const wrapper = document.getElementById("chat-wrapper");
const bubble = document.getElementById("chat-bubble");
let isDragging = false;
let startX, startY, initialX, initialY;

bubble.addEventListener("mousedown", (e) => {
    isDragging = false;
    startX = e.clientX;
    startY = e.clientY;
    
    // Lấy vị trí hiện tại của toàn bộ khối chat
    initialX = wrapper.offsetLeft;
    initialY = wrapper.offsetTop;

    function onMouseMove(e) {
        isDragging = true;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;

        // Di chuyển cả khối cha (bao gồm cả nút và màn hình chat)
        wrapper.style.left = (initialX + dx) + "px";
        wrapper.style.top = (initialY + dy) + "px";
        wrapper.style.bottom = "auto";
        wrapper.style.right = "auto";
    }

    function onMouseUp() {
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", onMouseUp);
        
        // Nếu không phải kéo mà là click thì mới đóng/mở chat
        if (!isDragging) toggleChat();
    }

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
});

// Chặn kéo ảnh
bubble.querySelector("img").draggable = false;


