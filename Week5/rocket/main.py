"""
uvicorn main:app --host 0.0.0.0 --port 8088 --reload
"""
import asyncio
import itertools
import math
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# 📐 กำหนดขนาดขอบเขตสนาม (600x800)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ⚔️ ค่าคงที่ของระบบต่อสู้ (ยิง/พลังชีวิต)
MAX_HP = 3
BULLET_SPEED = 14
BULLET_HIT_RADIUS = 22
GAME_TICK_SECONDS = 0.05  # ~20 ครั้งต่อวินาที


class RocketSpaceManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.rockets: Dict[str, dict] = {}
        self.bullets: Dict[str, dict] = {}
        self._bullet_ids = itertools.count()

    async def connect(self, rocket_id: str, websocket: WebSocket, is_dashboard: bool = False):
        await websocket.accept()
        self.connections[rocket_id] = websocket

        if not is_dashboard:
            # สุ่มตำแหน่งเริ่มต้นให้อยู่กลางๆ สนาม
            self.rockets[rocket_id] = {
                "x": SCREEN_WIDTH / 2,
                "y": SCREEN_HEIGHT / 2,
                "angle": 0,
                "hp": MAX_HP,
                "color": f"hsl({(hash(rocket_id) % 360)}, 80%, 60%)"
            }

        await websocket.send_json({
            "type": "INIT",
            "rockets": self.rockets,
            "bullets": self.bullets,
            "bounds": {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
        })

    def disconnect(self, rocket_id: str):
        if rocket_id in self.connections:
            del self.connections[rocket_id]
        if rocket_id in self.rockets:
            del self.rockets[rocket_id]

    async def broadcast(self, message: dict):
        for ws in list(self.connections.values()):
            try:
                await ws.send_json(message)
            except Exception:
                pass

    def spawn_bullet(self, owner_id: str):
        """ยิงกระสุนออกจากหัวจรวด ไปตามทิศทาง (angle) ปัจจุบันของจรวด"""
        rocket = self.rockets.get(owner_id)
        if not rocket:
            return

        rad = math.radians(rocket["angle"])
        nose_offset = 22  # ระยะจากจุดศูนย์กลางจรวดไปยังปลายหัว (ตามรูปทรงที่วาดใน dashboard)

        bullet_id = f"b{next(self._bullet_ids)}"
        self.bullets[bullet_id] = {
            "owner": owner_id,
            "x": rocket["x"] + nose_offset * math.cos(rad),
            "y": rocket["y"] + nose_offset * math.sin(rad),
            "vx": BULLET_SPEED * math.cos(rad),
            "vy": BULLET_SPEED * math.sin(rad),
        }

    async def game_tick(self):
        """เรียกทุก ๆ GAME_TICK_SECONDS: ขยับกระสุน, เช็คชนขอบ, เช็คโดนยิง แล้ว broadcast ผล"""
        to_remove = []
        hit_ids = []
        dead_ids = []

        for bullet_id, bullet in list(self.bullets.items()):
            bullet["x"] += bullet["vx"]
            bullet["y"] += bullet["vy"]

            out_of_bounds = (
                bullet["x"] < 0 or bullet["x"] > SCREEN_WIDTH
                or bullet["y"] < 0 or bullet["y"] > SCREEN_HEIGHT
            )
            if out_of_bounds:
                to_remove.append(bullet_id)
                continue

            for rocket_id, rocket in self.rockets.items():
                if rocket_id == bullet["owner"]:
                    continue  # ยิงโดนตัวเองไม่นับ
                if rocket_id in dead_ids:
                    continue  # โดนตายไปแล้วในติ๊กนี้ ไม่ต้องเช็คซ้ำ
                dx = rocket["x"] - bullet["x"]
                dy = rocket["y"] - bullet["y"]
                if (dx * dx + dy * dy) ** 0.5 <= BULLET_HIT_RADIUS:
                    to_remove.append(bullet_id)
                    rocket["hp"] -= 1
                    if rocket["hp"] <= 0:
                        dead_ids.append(rocket_id)
                    else:
                        hit_ids.append(rocket_id)
                    break

        for bullet_id in to_remove:
            self.bullets.pop(bullet_id, None)

        for rocket_id in hit_ids:
            await self.broadcast({"type": "HIT", "id": rocket_id, "rocket": self.rockets[rocket_id]})
        for rocket_id in dead_ids:
            await self.kill_rocket(rocket_id)

        await self.broadcast({"type": "TICK", "bullets": self.bullets})

    async def kill_rocket(self, rocket_id: str):
        """โดนยิงจน HP หมด: แจ้งทุกคนว่าใครตาย (พร้อมตำแหน่งล่าสุดไว้โชว์เอฟเฟกต์ระเบิด) แล้วตัดการเชื่อมต่อ
        ผู้เล่นคนนั้นทิ้ง — เขาต้องเข้าเกมใหม่ (รีเฟรชหน้าเว็บ) เองถึงจะได้จรวดใหม่ hp เต็ม ไม่ auto-respawn ให้"""
        last_known_state = self.rockets.get(rocket_id)
        await self.broadcast({"type": "DEAD", "id": rocket_id, "rocket": last_known_state})

        websocket = self.connections.get(rocket_id)
        if websocket is not None:
            try:
                await websocket.close()
            except Exception:
                pass
        # การปิด websocket ด้านบนจะทำให้ loop รับข้อมูลของผู้เล่นคนนี้ใน websocket_endpoint()
        # เจอ WebSocketDisconnect เอง ซึ่งจะไปเรียก manager.disconnect() + broadcast DESPAWN ต่อให้อัตโนมัติ


manager = RocketSpaceManager()


async def game_loop():
    """Background task เดียวที่คอยขยับกระสุน/เช็คโดนยิงตลอดเวลา ไม่ผูกกับ client คนไหนคนหนึ่ง"""
    while True:
        await asyncio.sleep(GAME_TICK_SECONDS)
        await manager.game_tick()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(game_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    is_dashboard = (client_id == "DASHBOARD")
    await manager.connect(client_id, websocket, is_dashboard)

    if not is_dashboard:
        await manager.broadcast({
            "type": "SPAWN",
            "id": client_id,
            "rocket": manager.rockets[client_id]
        })

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "CONTROL" and client_id in manager.rockets:
                rocket = manager.rockets[client_id]
                action = data["action"]

                speed = 8
                if action == "ROTATE_LEFT":
                    rocket["angle"] = (rocket["angle"] - 15) % 360
                elif action == "ROTATE_RIGHT":
                    rocket["angle"] = (rocket["angle"] + 15) % 360
                elif action == "THRUST":
                    rad = math.radians(rocket["angle"])

                    # คำนวณพิกัดใหม่
                    new_x = rocket["x"] + speed * math.cos(rad)
                    new_y = rocket["y"] + speed * math.sin(rad)

                    # 🔒 ล็อคพิกัดไม่ให้หลุดขอบ 800x600 (Padding 20px กันปีกจรวดเกิน)
                    rocket["x"] = max(20, min(SCREEN_WIDTH - 20, new_x))
                    rocket["y"] = max(20, min(SCREEN_HEIGHT - 20, new_y))
                elif action == "SHOOT":
                    manager.spawn_bullet(client_id)

                await manager.broadcast({
                    "type": "UPDATE",
                    "id": client_id,
                    "rocket": rocket
                })

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast({
            "type": "DESPAWN",
            "id": client_id
        })
