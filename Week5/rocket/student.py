import webbrowser
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Rocket Controller")

# หน้าจอควบคุมจรวด (HTML + CSS + JavaScript)
# หมายเหตุ: ไม่มี input() ฝั่ง Python แล้ว — ชื่อผู้เล่นถามผ่าน prompt() ในเบราว์เซอร์แทน
# และ URL ของเซิร์ฟเวอร์เกม (ws://.../ws/...) อ่านจาก window.location.hostname อัตโนมัติ
# ทำให้เพื่อนแค่เปิดเบราว์เซอร์เข้ามาที่ URL นี้ก็เล่นได้เลย ไม่ต้องรัน Python เอง
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rocket Controller</title>
    <style>
        body {
            background-color: #1e293b; color: white; font-family: sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0; user-select: none;
        }
        .info {
            text-align: center; margin-bottom: 20px;
        }
        .id-box {
            font-size: 24px; font-weight: bold; color: #38bdf8; background: #0f172a;
            padding: 8px 20px; border-radius: 8px; border: 1px solid #334155; display: inline-block; margin-top: 10px;
        }
        .controls { display: grid; grid-template-columns: repeat(3, 100px); gap: 15px; margin-top: 20px; }
        button {
            height: 80px; background: #3b82f6; border: none; border-radius: 12px;
            color: white; font-size: 20px; font-weight: bold; cursor: pointer;
            box-shadow: 0 4px #1d4ed8; transition: all 0.1s;
        }
        button:active { transform: translateY(4px); box-shadow: none; }
        .thrust { grid-column: span 3; background: #ef4444; box-shadow: 0 4px #b91c1c; font-size: 24px; }
        .shoot { grid-column: span 3; background: #f59e0b; box-shadow: 0 4px #b45309; font-size: 22px; }
    </style>
</head>
<body>

    <div class="info">
        <h2>Rocket Controller</h2>
        <div class="id-box" id="idBox">ID: -</div>
        <p id="connInfo" style="color: #94a3b8; font-size: 14px;"></p>
        <p>ใช้ปุ่มด้านล่าง หรือปุ่มลูกศร (← → ↑) และ Spacebar (ยิง) บนคีย์บอร์ดเพื่อขับจรวด</p>
    </div>

    <div class="controls">
        <button onclick="sendControl('ROTATE_LEFT')">↺ Left</button>
        <div></div>
        <button onclick="sendControl('ROTATE_RIGHT')">Right ↻</button>
        <button class="thrust" onclick="sendControl('THRUST')">🔥 THRUST 🔥</button>
        <button class="shoot" onclick="sendControl('SHOOT')">🔫 SHOOT</button>
    </div>

<script>
    // 1. ถามชื่อ/รหัสนักศึกษาผ่านหน้าเว็บ (ไม่ใช่ input() ของ Python อีกต่อไป)
    let studentId = "";
    while (!studentId) {
        studentId = (window.prompt("กรุณาใส่ชื่อ/รหัสนักศึกษาของคุณ:") || "").trim();
    }
    document.getElementById('idBox').innerText = "ID: " + studentId;

    // 2. เชื่อมต่อไปยัง Server หลัก (Port 8088) โดยใช้ host เดียวกับที่เปิดหน้านี้อยู่โดยอัตโนมัติ
    const serverHost = window.location.hostname || "localhost";
    document.getElementById('connInfo').innerText =
        `เชื่อมต่อไปยัง: ws://${serverHost}:8088/ws/${studentId}`;
    const ws = new WebSocket(`ws://${serverHost}:8088/ws/${studentId}`);

    // ถ้าโดนยิงจน HP หมด เซิร์ฟเวอร์จะปิดการเชื่อมต่อนี้ทิ้ง -> แจ้งเตือนแล้วโหลดหน้าใหม่เพื่อเข้าเกมอีกครั้ง
    let diedOnPurpose = false;
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'DEAD' && data.id === studentId) {
            diedOnPurpose = true;
        }
    };
    ws.onclose = () => {
        if (diedOnPurpose) {
            alert('💀 คุณถูกยิงจน HP หมดแล้ว! กด OK เพื่อเข้าเกมใหม่');
        }
        location.reload();
    };

    function sendControl(action) {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'CONTROL',
                action: action
            }));
        }
    }

    // รองรับการกดปุ่มบนคีย์บอร์ด (Arrow Keys + Space สำหรับยิง)
    window.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') sendControl('ROTATE_LEFT');
        if (e.key === 'ArrowRight') sendControl('ROTATE_RIGHT');
        if (e.key === 'ArrowUp') sendControl('THRUST');
        if (e.code === 'Space') {
            e.preventDefault();  // กัน browser เลื่อนหน้าจอตอนกด space
            sendControl('SHOOT');
        }
    });
</script>
</body>
</html>
"""

@app.get("/")
async def get_index():
    return HTMLResponse(html_code)

if __name__ == "__main__":
    # host="0.0.0.0" ทำให้เพื่อนในวง LAN เดียวกันเปิดเบราว์เซอร์เข้ามาที่ IP ของเครื่องนี้ได้โดยตรง
    # เช่น http://172.20.48.132:8002/ โดยไม่ต้องติดตั้ง Python/รันไฟล์นี้เอง
    client_port = 8002
    webbrowser.open(f"http://127.0.0.1:{client_port}")
    uvicorn.run(app, host="0.0.0.0", port=client_port)
