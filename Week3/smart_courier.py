# Assignment 1: Smart Courier System (40 คะแนน)
# Objective: ตรวจสอบการคุมและการจัดการ CancelledError
# Skills: create_task + name, .done(), .cancel(), CancelledError, .cancelled()

import asyncio
from time import ctime


# ──────────────────────────────────────────────
# ข้อ 1: Coroutine function ที่จำลองการส่งพัสดุ
# ──────────────────────────────────────────────
async def delivery_task(package_id, duration):
    """
    จำลองพนักงานส่งพัสดุ 1 คน
    - พิมพ์ข้อความเมื่อเริ่มส่ง
    - รอ asyncio.sleep(duration) แทนการเดินทางจริง
    - ดักจับ CancelledError เพื่อล้างทรัพยากรและแจ้งผล
    - return ข้อความยืนยันเมื่อสำเร็จ
    """
    try:
        print(f"{ctime()} Courier started delivering {package_id}...")
        await asyncio.sleep(duration)  # จุดสลับ — Event Loop สามารถสั่ง cancel ได้ที่นี่
        print(f"{ctime()} Package {package_id} Delivered!")
        return f"Package {package_id} Delivered!"

    except asyncio.CancelledError:
        # ──────────────────────────────────────────────────────
        # ข้อ 5: ดักจับ CancelledError และพิมพ์ข้อความแจ้งเตือน
        # ──────────────────────────────────────────────────────
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        raise  # ต้อง re-raise เสมอ เพื่อให้ Task ถูกทำเครื่องหมายว่า "cancelled" จริงๆ


# ──────────────────────────────────────────────
# ฟังก์ชันหลัก
# ──────────────────────────────────────────────
async def main():
    # ──────────────────────────────────────────────────────────
    # ข้อ 2: สร้าง Task จาก delivery_task ตั้งชื่อว่า "Express-Courier"
    # ──────────────────────────────────────────────────────────
    task = asyncio.create_task(
        delivery_task("P001", duration=5.0),
        name="Express-Courier"           # ตั้งชื่อ Task ตามข้อกำหนด
    )

    # ──────────────────────────────────────────────────────────
    # ข้อ 3: รอ 2 วินาที แล้วตรวจสอบสถานะ Task
    # ──────────────────────────────────────────────────────────
    await asyncio.sleep(2.0)

    print(f"{ctime()} Checking task '{task.get_name()}'. Is it done? {task.done()}")

    # ──────────────────────────────────────────────────────────
    # ข้อ 4: ถ้ายังไม่เสร็จ ให้ยกเลิกทันที
    # ──────────────────────────────────────────────────────────
    if not task.done():
        print(f"{ctime()} Taking too long! Canceling the task...")
        task.cancel()

    # yield ให้ Event Loop มีโอกาสส่ง CancelledError เข้าไปใน delivery_task
    await asyncio.sleep(0.1)

    # ──────────────────────────────────────────────────────────
    # ข้อ 5: ตรวจสอบสถานะสุดท้ายด้วย .cancelled()
    # ──────────────────────────────────────────────────────────
    print(f"{ctime()} Final verify: Is task officially canceled? {task.cancelled()}")


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())