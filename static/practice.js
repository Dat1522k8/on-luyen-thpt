// --- BIẾN TOÀN CỤC ---
let danh_sach_cau_hoi = [];
let cau_sai_list = [];
let timerInterval;

// --- 1. LOGIC TẢI ĐỀ TỰ DO ---
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
        renderQuiz(danh_sach_cau_hoi);
        batDauDemNguoc(so_cau * 120);
    });
}

// --- 2. LOGIC CHAT AI & PHÂN TÍCH ---
function guiTinNhanAI() {
    const input = document.getElementById("ai_input");
    let userMsg = input.value.trim();
    if (!userMsg) return;

    renderMessage("user", userMsg);
    input.value = "";

    let match = userMsg.match(/giải câu (\d+)/i);
    let extraContext = "";
    if (match) {
        let soCau = parseInt(match[1]);
        let cauHoiGoc = danh_sach_cau_hoi[soCau - 1]; 
        if (cauHoiGoc) extraContext = `\n(Đề bài: ${cauHoiGoc.question}. Đáp án đúng: ${cauHoiGoc.answer})`;
    }

    fetch("/chat_ai", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ message: userMsg + extraContext, user_name: window.userName })
    }).then(res => res.json()).then(data => renderMessage("ai", data.answer));
}

function phanTichAI() {
    if (!cau_sai_list.length) return alert("Bạn chưa làm sai câu nào!");
    document.getElementById("ai-panel").style.display = "flex";
    let danhSachSoCau = cau_sai_list.map(sai => {
        let index = danh_sach_cau_hoi.findIndex(q => q.question === sai.cau_hoi);
        return `Câu ${index + 1}`;
    }).join(", ");

    renderMessage("ai", `Đang check list lỗi sai của bro...`);
    fetch("/chat_ai", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ 
            message: `[ANALYSIS] Học sinh làm sai: ${danhSachSoCau}. Hãy liệt kê và chào hỏi, đừng giải ngay.`, 
            user_name: window.userName 
        })
    }).then(res => res.json()).then(data => renderMessage("ai", data.answer));
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