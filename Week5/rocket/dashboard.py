import webbrowser
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

server_ip = input("กรุณากรอก IP ของ Server (กด Enter หากเป็น localhost): ").strip() or "localhost"

app = FastAPI(title="Mission Control Dashboard")

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🚀 Rocket Space Dashboard (800x600)</title>
    <style>
        body {{
            margin: 0; background-color: #0b0f19; color: white; font-family: sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            min-height: 100vh;
        }}
        #header {{ margin-bottom: 10px; text-align: center; }}
        #header h1 {{ margin: 0; font-size: 24px; }}
        #counter {{ font-size: 16px; color: #38bdf8; font-weight: bold; }}
        
        /* กำหนดขนาดกรอบ Canvas 800x600 */
        #canvas-container {{
            border: 3px solid #38bdf8;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
            overflow: hidden;
        }}
        canvas {{ display: block; background: radial-gradient(circle, #1a233a 0%, #0b0f19 100%); }}
    </style>
</head>
<body>

<div id="header">
    <h1>Mission Control Dashboard</h1>
    <div id="counter">Active Rockets: 0 | Arena: 800 x 600</div>
</div>

<div id="canvas-container">
    <canvas id="space" width="800" height="600"></canvas>
</div>

<script>
    const canvas = document.getElementById('space');
    const ctx = canvas.getContext('2d');

    const MAX_HP = 3;
    const rockets = {{}};
    const bullets = {{}};
    const explosions = [];  // {{x, y, start}} เอฟเฟกต์วงระเบิดตอนมีคนตาย
    const ws = new WebSocket("ws://{server_ip}:8088/ws/DASHBOARD");

    ws.onmessage = (event) => {{
        const data = JSON.parse(event.data);

        if (data.type === 'INIT') {{
            Object.assign(rockets, data.rockets);
            Object.assign(bullets, data.bullets || {{}});
        }} else if (data.type === 'SPAWN' || data.type === 'UPDATE' || data.type === 'HIT') {{
            rockets[data.id] = data.rocket;
        }} else if (data.type === 'DEAD') {{
            if (data.rocket) {{
                explosions.push({{ x: data.rocket.x, y: data.rocket.y, start: performance.now() }});
            }}
            delete rockets[data.id];
        }} else if (data.type === 'DESPAWN') {{
            delete rockets[data.id];
        }} else if (data.type === 'TICK') {{
            for (const key of Object.keys(bullets)) delete bullets[key];
            Object.assign(bullets, data.bullets);
        }}

        document.getElementById('counter').innerText = `Active Rockets: ${{Object.keys(rockets).length}} | Arena: 800 x 600`;
    }};

    function drawRocket(x, y, angle, color, id) {{
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angle * Math.PI / 180);

        ctx.beginPath();
        ctx.moveTo(20, 0);
        ctx.lineTo(-15, -12);
        ctx.lineTo(-8, 0);
        ctx.lineTo(-15, 12);
        ctx.closePath();

        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.restore();

        ctx.fillStyle = '#ffffff';
        ctx.font = '12px monospace';
        ctx.fillText(id, x - 20, y - 25);
    }}

    function drawHearts(x, y, hp) {{
        const clampedHp = Math.max(0, Math.min(MAX_HP, hp ?? MAX_HP));
        const heartsText = '❤'.repeat(clampedHp) + '♡'.repeat(MAX_HP - clampedHp);
        ctx.fillStyle = '#ef4444';
        ctx.font = '14px sans-serif';
        ctx.fillText(heartsText, x - 20, y - 40);
    }}

    function drawBullet(x, y) {{
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#fbbf24';
        ctx.fill();
    }}

    function drawExplosions() {{
        const now = performance.now();
        for (let i = explosions.length - 1; i >= 0; i--) {{
            const exp = explosions[i];
            const t = (now - exp.start) / 500;  // แสดงผลรวม 500ms แล้วหายไป
            if (t >= 1) {{
                explosions.splice(i, 1);
                continue;
            }}
            ctx.beginPath();
            ctx.arc(exp.x, exp.y, 10 + t * 30, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(251, 191, 36, ${{1 - t}})`;
            ctx.lineWidth = 4;
            ctx.stroke();
        }}
    }}

    function drawGrid(gridSize = 50) {{
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.lineWidth = 1;

        for (let x = 0; x < canvas.width; x += gridSize) {{
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }}

        for (let y = 0; y < canvas.height; y += gridSize) {{
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }}
    }}

    function render() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        drawGrid(50);

        for (const [id, rocket] of Object.entries(rockets)) {{
            drawRocket(rocket.x, rocket.y, rocket.angle, rocket.color, id);
            drawHearts(rocket.x, rocket.y, rocket.hp);
        }}

        for (const bullet of Object.values(bullets)) {{
            drawBullet(bullet.x, bullet.y);
        }}

        drawExplosions();

        requestAnimationFrame(render);
    }}
    render();
</script>
</body>
</html>
"""

@app.get("/")
async def get_dashboard():
    return HTMLResponse(html_code)

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
    
    