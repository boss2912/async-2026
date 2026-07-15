import asyncio
import aiohttp
from time import time, ctime   # เพิ่มเข้ามาเพื่อทำ output ให้ตรงฟอร์แมตเดียวกับไฟล์อื่น

STUDENT_ID = "6710301006"  # TODO: เปลี่ยนเป็นรหัสนักศึกษาของตัวเองให้ตรง
BASE_URL = "http://172.16.2.117:8088"   # <-- ใช้ IP และ port นี้แทน 127.0.0.1:8000


async def turn_on_light(session, light_id):
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"

    # เพิ่ม: แจ้งก่อนส่ง request (เนื่องจากรันพร้อมกันผ่าน gather บรรทัดนี้
    # ของทั้ง 4 ดวงจะขึ้นพร้อมๆ กันเกือบทันที ก่อนใครจะ 'ติด' จริง)
    print(f"{ctime()} [Sending] Turning ON {light_id} ...")

    async with session.post(url, json={"status": "ON"}) as resp:
        data = await resp.json()
        # เปลี่ยนแค่รูปแบบ print ให้มี ctime() + [Confirmed] เหมือนไฟล์อื่น (logic เดิมทุกอย่าง)
        print(f"{ctime()} [Confirmed] {light_id} status = {data['current_status']}")


async def main():
    print(f"{ctime()} --- [Task] Turning ON all 4 lights CONCURRENTLY (gather) ---")

    # เพิ่ม: จับเวลาก่อนเริ่ม gather
    start_time = time()

    async with aiohttp.ClientSession() as session:
        # โครงสร้างเดิม ไม่แก้ไข: gather ทั้ง 4 ดวงพร้อมกัน
        await asyncio.gather(
            turn_on_light(session, "light_1"),
            turn_on_light(session, "light_2"),
            turn_on_light(session, "light_3"),
            turn_on_light(session, "light_4"),
        )

    # เพิ่ม: คำนวณและแสดงเวลารวมท้ายโปรแกรม
    elapsed = time() - start_time
    print(f"{ctime()} --- All lights turned ON successfully (concurrent) ---")
    print(
        f"{ctime()} Total time: {elapsed:.2f} seconds "
        "(Equals to the slowest light's delay, since all requests run concurrently)."
    )


asyncio.run(main())