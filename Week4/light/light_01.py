import asyncio
import aiohttp
from time import time, ctime   # เพิ่มเข้ามาเพื่อทำ output ให้ตรงฟอร์แมตเดียวกับไฟล์อื่น

STUDENT_ID = "6710301006"  # TODO: เปลี่ยนเป็นรหัสนักศึกษาของตัวเองให้ตรง
BASE_URL = "http://172.16.2.117:8088"


async def turn_on_light(session, light_id):
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"

    # เพิ่ม: แจ้งก่อนส่ง request ออกไป (ให้ตรงฟอร์แมต [Sending] เหมือนไฟล์อื่น)
    print(f"{ctime()} [Sending] Turning ON {light_id} ...")

    async with session.post(url, json={"status": "ON"}) as resp:
        data = await resp.json()
        # เปลี่ยนแค่รูปแบบ print ให้มี ctime() + [Confirmed] เหมือนไฟล์อื่น (logic เดิมทุกอย่าง)
        print(f"{ctime()} [Confirmed] {light_id} status = {data['current_status']}")


async def main():
    print(f"{ctime()} --- [Task] Turning ON lights in order: light_1 -> light_4 ---")

    # เพิ่ม: จับเวลาก่อนเริ่มคำสั่ง await ตัวแรก
    start_time = time()

    async with aiohttp.ClientSession() as session:
        # รอทีละดวง เรียงตามลำดับ 1 -> 2 -> 3 -> 4 (โครงสร้างเดิม ไม่แก้ไข)
        await turn_on_light(session, "light_1")
        await turn_on_light(session, "light_2")
        await turn_on_light(session, "light_3")
        await turn_on_light(session, "light_4")

    # เพิ่ม: คำนวณและแสดงเวลารวมท้ายโปรแกรม เหมือนไฟล์อื่น
    elapsed = time() - start_time
    print(f"{ctime()} --- All lights turned ON successfully in order ---")
    print(
        f"{ctime()} Total time: {elapsed:.2f} seconds "
        "(Sum of all delays, since lights are turned on sequentially)."
    )


asyncio.run(main())