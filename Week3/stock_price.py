# Assignment 3: Stock Price Race (Live FastAPI + HTTPX) (10 คะแนน)
# Objective: ประยุกต์ใช้ Concurrency บนระบบเครือข่ายจำลองจริงร่วมกับ httpx
# Skills: httpx.AsyncClient, create_task, asyncio.wait + FIRST_COMPLETED, .cancel()
#
# ก่อนรันไฟล์นี้ ต้องเปิด Mock Server ก่อนในอีก Terminal หนึ่ง:
#   uvicorn stock_api:app --reload --port 8088

import asyncio
import httpx
from time import ctime


# ──────────────────────────────────────────────
# ข้อ 1: Coroutine function เชื่อมต่อ Mock Server ผ่านระบบเครือข่ายจริง
# ──────────────────────────────────────────────
async def fetch_stock_price(server_name: str):
    """
    เชื่อมต่อไปยัง Stock Price API Server ของอาจารย์ (FastAPI, พอร์ต 8088)
    - ห้ามรับพารามิเตอร์ delay (latency เกิดขึ้นจริงที่ฝั่ง Server แล้ว)
    - ใช้ httpx.AsyncClient() แบบ async with เพื่อไม่ Block Event Loop
    - แปลง JSON ที่ได้ (server, price_usd) มาจัดฟอร์แมตเป็นข้อความ
    """
    url = f"http://127.0.0.1:8088/price/{server_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"


# ──────────────────────────────────────────────
# ฟังก์ชันหลัก: Concurrency Racing
# ──────────────────────────────────────────────
async def main():
    # ──────────────────────────────────────────────────────────
    # ข้อ 2: แปลงคอรูทีนของทั้ง 3 สาขาให้เป็น asyncio.Task
    #         เพื่อส่งเข้าคิวรันพร้อมกันใน Event Loop
    # ──────────────────────────────────────────────────────────
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha")),
        asyncio.create_task(fetch_stock_price("Beta")),
        asyncio.create_task(fetch_stock_price("Gamma")),
    }

    # ──────────────────────────────────────────────────────────
    # ข้อ 3: ใช้ asyncio.wait() + FIRST_COMPLETED เพื่อดีดตัวออกทันที
    #         เมื่อมีเซิร์ฟเวอร์ตัวแรกส่งข้อมูลกลับมาสำเร็จ
    # ──────────────────────────────────────────────────────────
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )

    # ──────────────────────────────────────────────────────────
    # ข้อ 4: แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน
    # ──────────────────────────────────────────────────────────
    for winner in done:
        print(f"{ctime()} Winner Result: {winner.result()}")

    # ──────────────────────────────────────────────────────────
    # ข้อ 5: [สำคัญมาก - Anti-Memory Leak]
    #         วนลูปดึงงานที่ยังค้างอยู่ใน pending มาสั่งยกเลิกทิ้งให้หมดสิ้น
    #         เพื่อตัดสัญญาณ Network Request ที่ยังวิ่งค้างอยู่บนระบบเครือข่าย
    # ──────────────────────────────────────────────────────────
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")

    for task in pending:
        task.cancel()


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
asyncio.run(main())