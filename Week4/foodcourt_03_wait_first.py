# foodcourt_03_wait_first.py
import asyncio
import time
from time import ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301006"
    print(f"{ctime()} | --- [Task 3] Practice using wait to wait for the first completed order ---")

    start = time.perf_counter()

    # 1) สร้าง Task สำหรับ 3 ออเดอร์ (ต้องเป็น Task ไม่ใช่ coroutine เฉยๆ)
    orders = [
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Mixed")),
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")),
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak")),
    ]

    # 2) รอจนกว่าจะมีตัวแรกเสร็จ (ไม่ต้องรอทุกตัว)
    done, pending = await asyncio.wait(orders, return_when=asyncio.FIRST_COMPLETED)

    # Get the result of the first completed order
    winner_task = done.pop()
    fastest_dish = winner_task.result()
    print(f"{ctime()} | Winner served dish: Shop: {fastest_dish['shop']} | Menu: {fastest_dish['menu']}")

    # 3) ยกเลิกตัวที่ยังค้างอยู่
    print(f"{ctime()} | Cleaning up: Canceling {len(pending)} remaining pending orders...")
    for task in pending:
        task.cancel()

    await asyncio.gather(*pending, return_exceptions=True)

    elapsed = time.perf_counter() - start
    print(f"{ctime()} | Total waiting time for the first dish: {elapsed:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())