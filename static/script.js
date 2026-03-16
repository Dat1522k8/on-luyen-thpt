let danh_sach_cau_hoi = [];
let cau_dang_xem = null;

function taiConcept() {
    let mon = document.getElementById("mon").value;
    fetch("/concepts?mon=" + mon)
        .then(res => res.json())
        .then(data => {
            let select = document.getElementById("concept");
            select.innerHTML = '<option value="all">Tất cả chủ đề</option>';
            data.forEach(c => {
                let op = document.createElement("option");
                op.value = c; op.text = c;
                select.appendChild(op);
            });
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
            html += `<div class="question-card" onclick="setCtx(${i})">
                <h3>Câu ${i+1}</h3>
                <div class="question-text">${q.question}</div>
                <div class="options-container">`; // Bọc các phương án
            q.options.forEach(opt => {
                html += `
                <label class="option">
                    <input type="radio" name="cau${i}" value="${opt}" onchange="setCtx(${i})">
                    <span>${opt}</span>
                </label>`;
            });
            html += `</div></div>`;
        });
        document.getElementById("de").innerHTML = html;
        if (window.MathJax) MathJax.typesetPromise();
    });
}

function setCtx(i) {
    let q = danh_sach_cau_hoi[i];
    let chk = document.querySelector(`input[name="cau${i}"]:checked`);
    cau_dang_xem = {
        question: q.question,
        correct_answer: q.answer,
        student_choice: chk ? chk.value : "Chưa chọn"
    };
}
function hoiNhanh(i) {
    setCtx(i); // Gắn ngữ cảnh câu hỏi thứ i
    moAI();    // Mở Panel AI

    let input = document.getElementById("ai_input");
    input.value = "Giải thích cho em kỹ hơn về câu này...";
    input.focus(); // Đưa con trỏ vào ô nhập để bạn có thể xóa hoặc viết tiếp

    // Thông báo cho người dùng biết AI đang tập trung vào câu nào
    document.getElementById("chatbox").innerHTML += `
        <div style="text-align:center; color:#4facfe; font-size:12px; margin:10px 0; border-bottom: 1px dashed #4facfe;">
            --- Đang tập trung giải thích Câu ${i+1} ---
        </div>`;
}
function guiTinNhanAI() {
    let input = document.getElementById("ai_input");
    let msg = input.value.trim();
    if (!msg) return;

    document.getElementById("chatbox").innerHTML += `
        <div style="margin-bottom:15px; text-align:right;">
            <span style="background:#4facfe; color:white; padding:8px 12px; border-radius:12px; display:inline-block;">
                ${msg}
            </span>
        </div>`;

    input.value = ""; 

    fetch("/chat_ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: msg,
            context: cau_dang_xem 
        })
    })
    .then(res => res.json())
    .then(data => {
        // KIỂM TRA NẾU CÓ LỖI TỪ SERVER
        let phan_hoi = data.answer || "AI không trả về câu trả lời. Vui lòng kiểm tra API Key.";
        
        document.getElementById("chatbox").innerHTML += `
            <div style="margin-bottom:15px; display: flex; flex-direction: column;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 5px;">
                    <img src="/static/cheems.jpg" style="width: 25px; height: 25px; border-radius: 50%; object-fit: cover; border: 1px solid #ddd;">
                    <b style="color:#ff7a18;">cheems AI:</b>
                </div>
                <div style="background:#f1f1f1; padding:10px; border-radius:8px; margin-left: 33px;">
                    ${phan_hoi}
                </div>
            </div>`;

        let chatbox = document.getElementById("chatbox");
        chatbox.scrollTop = chatbox.scrollHeight;
        if (window.MathJax) MathJax.typesetPromise();
    })
    .catch(err => {
        console.error("Lỗi Fetch:", err);
        document.getElementById("chatbox").innerHTML += `<div style="color:red; text-align:center;">Lỗi kết nối Server!</div>`;
    });
}

// Các hàm khác (initResizer, nopBai, phanTichAI, moAI, dongAI, moChatTuDo) giữ nguyên như bản trước...
function initResizer() {
    const resizer = document.getElementById("resizer");
    const aiPanel = document.getElementById("ai-panel");
    let isResizing = false;
    resizer.addEventListener("mousedown", () => { isResizing = true; document.body.style.cursor = "col-resize"; });
    document.addEventListener("mousemove", (e) => {
        if (!isResizing) return;
        let newWidth = window.innerWidth - e.clientX;
        if (newWidth > 300 && newWidth < window.innerWidth * 0.7) aiPanel.style.width = newWidth + "px";
    });
    document.addEventListener("mouseup", () => { isResizing = false; document.body.style.cursor = "default"; });
}

function nopBai() {
    let ans = [];
    for(let i=0; i<danh_sach_cau_hoi.length; i++) {
        let chk = document.querySelector(`input[name="cau${i}"]:checked`);
        if(!chk) { alert("Làm hết bài đã nhé!"); return; }
        ans.push(chk.value);
    }
    fetch("/nop_bai", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({cau_tra_loi: ans}) })
    .then(res => res.json())
    .then(data => {
        let html = `<h2>Kết quả: ${data.diem}/${danh_sach_cau_hoi.length}</h2>`;
        data.ket_qua.forEach((kq, i) => {
            let color = kq.dung ? "green" : "red";
            html += `<div class="question-card" style="border-left-color:${color}">
                <b>Câu ${i+1}:</b> ${kq.cau_hoi}<br>
                Chọn: <span style="color:${color}">${kq.tra_loi_cua_ban}</span> | Đáp án: ${kq.dap_an_dung}<br>
                <button onclick="hoiNhanh(${i})">💡 Giải thích</button>
            </div>`;
        });
        document.getElementById("ketqua").innerHTML = html;
        if (window.MathJax) MathJax.typesetPromise();
    });
}

function phanTichAI() {
    moAI();
    let cauSai = [];
    danh_sach_cau_hoi.forEach((q, i) => {
        let chk = document.querySelector(`input[name="cau${i}"]:checked`);
        if (chk && chk.value != q.answer) cauSai.push(q.question);
    });
    fetch("/ai_lo_trinh", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({cau_sai: cauSai}) })
    .then(res => res.json())
    .then(data => {
        document.getElementById("chatbox").innerHTML += `<div style="background:#f0f7ff; padding:15px; border-radius:8px; margin-bottom:10px;"><b>🤖 Lộ trình AI:</b><br>${data.answer}</div>`;
        document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
        if (window.MathJax) MathJax.typesetPromise();
    });
}

function hoiNhanh(i) { setCtx(i); moAI(); document.getElementById("ai_input").value = "Tại sao câu này em làm sai?"; guiTinNhanAI(); }
function moAI() { document.getElementById("main-wrapper").classList.add("split"); }
function dongAI() { document.getElementById("main-wrapper").classList.remove("split"); }
function moChatTuDo() { cau_dang_xem = null; moAI(); document.getElementById("chatbox").innerHTML += `<div style="text-align:center; color:#888;">--- Chat tự do ---</div>`; }

document.addEventListener("DOMContentLoaded", () => {
    initResizer();
    taiConcept();
    document.getElementById("mon").addEventListener("change", taiConcept);
    document.getElementById("ai_input").addEventListener("keydown", (e) => { if(e.key === "Enter") { e.preventDefault(); guiTinNhanAI(); } });
});