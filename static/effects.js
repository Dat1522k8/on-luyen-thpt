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