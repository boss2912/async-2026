# Assignment 2: Stock Price Race (Mock Version) (50 คะแนน)
# Objective: ตรวจสอบลอจิก FIRST_COMPLETED ผ่าน asyncio.sleep
# หมายเหตุ: นักเรียนต้องเลือกใช้ asyncio.wait() พร้อมออปชัน
# return_when=asyncio.FIRST_COMPLETED เท่านั้น (ห้ามใช้ gather หรือ wait_for)

import asyncio
from time import ctime


# ──────────────────────────────────────────────
# ข้อ 1: Coroutine function ดึงราคาหุ้นจำลอง
# ──────────────────────────────────────────────
async def fetch_stock_price(server_name, delay):
    """
    จำลองการเชื่อมต่อไปยังเซิร์ฟเวอร์สาขาต่างๆ เพื่อดึงราคาหุ้น
    - ใช้ asyncio.sleep(delay) แทนเวลาหน่วงของเครือข่ายจริง
    - คืนค่าเป็นข้อความราคาหุ้นเมื่อดึงข้อมูลสำเร็จ
    """
    await asyncio.sleep(delay)  # จุดสลับ — Event Loop สามารถสั่ง cancel งานนี้ได้ที่นี่
    return f"[{server_name}] Price: 150 USD"


# ──────────────────────────────────────────────
# ฟังก์ชันหลัก
# ──────────────────────────────────────────────
async def main():
    # ──────────────────────────────────────────────────────────
    # ข้อ 2: สร้าง 3 Tasks พร้อมกันในระบบ (Alpha, Beta, Gamma)
    # ──────────────────────────────────────────────────────────
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0), name="Alpha"),
        asyncio.create_task(fetch_stock_price("Beta", 0.8), name="Beta"),
        asyncio.create_task(fetch_stock_price("Gamma", 1.5), name="Gamma"),
    }

    # ──────────────────────────────────────────────────────────
    # ข้อ 3: ใช้ asyncio.wait() + FIRST_COMPLETED เพื่อดีดตัวออก
    #         ทันทีที่เซิร์ฟเวอร์ตัวแรกตอบกลับสำเร็จ
    # ──────────────────────────────────────────────────────────
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # ──────────────────────────────────────────────────────────
    # ข้อ 4: แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน
    # ──────────────────────────────────────────────────────────
    winner_task = done.pop()
    print(f"{ctime()} Winner Result: {winner_task.result()}")

    # ──────────────────────────────────────────────────────────
    # ข้อ 5: วนลูปยกเลิก Task ที่เหลือใน pending ทั้งหมด
    #         เพื่อป้องกัน Memory Leak
    # ──────────────────────────────────────────────────────────
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for ongoing_task in pending:
        ongoing_task.cancel()

    # yield ให้ Event Loop มีโอกาสประมวลผลการ cancel ให้เสร็จสมบูรณ์
    await asyncio.gather(*pending, return_exceptions=True)


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())