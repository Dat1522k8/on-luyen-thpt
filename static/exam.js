let currentQuizData = [];
let correctAnswers = [];

// --- 1. TẢI ĐỀ THEO MÃ (Lấy từ URL) ---
async function loadExamByCode() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    const res = await fetch(`/api/get-quiz?code=${code}`);
    const data = await res.json();
    
    if(data.error) return alert("Mã đề sai rồi Đạt ơi!");

    currentQuizData = data.questions;
    correctAnswers = data.questions.map(q => q.answer);
    
    // Hiển thị giao diện đề thi (Render HTML)
    renderExamInterface(data);
    startTimer(data.info.time_limit);
}

// --- 2. NỘP BÀI VÀ LƯU CSV ---
async function submitExam() {
    let score = 0;
    let details = [];
    
    currentQuizData.forEach((q, i) => {
        let chk = document.querySelector(`input[name="cau${i}"]:checked`);
        let userAns = chk ? chk.value : "X";
        
        if(userAns === correctAnswers[i]) {
            score++;
            details.push(`C${i+1}:Đ`);
        } else {
            details.push(`C${i+1}:S`);
        }
    });

    const finalScore = ((score / currentQuizData.length) * 10).toFixed(2);
    const urlParams = new URLSearchParams(window.location.search);

    // Gửi về Server để ghi file CSV riêng cho mã đề
    await fetch("/api/submit-exam", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            quiz_code: urlParams.get('code'),
            score: finalScore,
            details: details.join(", ")
        })
    });

    alert(`Kết quả của bạn: ${finalScore}/10. Điểm đã được gửi cho giáo viên!`);
    window.location.href = "/student-hub";
}