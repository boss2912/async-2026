import asyncio
import httpx
from time import time, ctime

# ==========================================
# 1. Configuration & Constants
# ==========================================
STUDENT_ID = "6710301006"
BASE_URL = "http://172.16.2.117:8088"

# กำหนดลำดับชิ้นส่วนและหุ่นยนต์
PARTS = ["A", "B", "C"]
ROBOTS = ["robot_1", "robot_2", "robot_3", "robot_4"]

# ==========================================
# 2. Async Functions Development
# ==========================================

async def reset_factory(client: httpx.AsyncClient):
    """ส่ง Request เพื่อทำการ Reset สถานะของหุ่นยนต์ทั้งหมดของรหัสนักเรียนนี้"""
    print(f"{ctime()} [Sending] Resetting factory ...")
    response = await client.post(f"/student/{STUDENT_ID}/reset")
    data = response.json()
    print(f"{ctime()} [Confirmed] Factory reset done.")
    return data

async def grab_part(client: httpx.AsyncClient, robot_id: str, part: str):
    """สั่งให้หุ่นยนต์หยิบชิ้นส่วน 1 ชิ้น"""
    print(f"{ctime()} [Sending] {robot_id} grabbing part {part} ...")
    response = await client.post(
        f"/student/{STUDENT_ID}/robot/{robot_id}/grab",
        json={"part": part},
    )
    data = response.json()
    print(f"{ctime()} [Confirmed] {robot_id} grabbed {part} -> {data.get('status')}")
    return data

async def run_robot_task(client: httpx.AsyncClient, robot_id: str):
    """สั่งให้หุ่นยนต์ 1 ตัว ทำการหยิบชิ้นส่วน A, B, และ C ตามลำดับ"""
    results = []
    for part in PARTS:
        result = await grab_part(client, robot_id, part)
        results.append(result)
    return results

async def main():
    """ฟังก์ชันหลักสำหรับเริ่มการทำงานของหุ่นยนต์ทั้ง 4 ตัวแบบ Async"""
    program_start = time()

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print(f"{ctime()} --- [Task] Resetting Factory ---")
        await reset_factory(client)

        print(f"{ctime()} --- [Task] Running {len(ROBOTS)} robots CONCURRENTLY (gather) ---")
        gather_start = time()

        tasks = [run_robot_task(client, robot_id) for robot_id in ROBOTS]
        results = await asyncio.gather(*tasks)

        gather_elapsed = time() - gather_start
        total_elapsed = time() - program_start

        print(f"{ctime()} --- All robots finished (concurrent) ---")
        print(
            f"{ctime()} Robots time: {gather_elapsed:.2f} seconds "
            "(Equals to the slowest robot's total delay, since all robots run concurrently)."
        )
        print(f"{ctime()} Total time (reset + robots): {total_elapsed:.2f} seconds")
        for robot_id, result in zip(ROBOTS, results):
            print(f"{robot_id}: {result}")

if __name__ == "__main__":
    asyncio.run(main())
