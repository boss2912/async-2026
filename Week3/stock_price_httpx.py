import asyncio
import httpx
from time import ctime


async def fetch_stock_price(server_name: str):
<<<<<<< HEAD
    url = f"http://127.0.0.1:8088/price/{server_name}"

=======
    """
    TODO: Assignment 3 - เขียนฟังก์ชันเชื่อมต่อ Mock Server ผ่านระบบเครือข่าย
    1. กำหนดเป้าหมายไปที่พอร์ต 8088 ตามสเปกเซิร์ฟเวอร์ของอาจารย์
    2. ใช้ httpx.AsyncClient() ดึงข้อมูลเพื่อไม่ให้เกิดการ Block สัญญาณ Event Loop
    3. นำข้อมูล JSON (server และ price_usd) มาจัดฟอร์แมตแสดงผล
    """
    url = f"http://127.0.0.1:8088/price/{server_name}"
    
>>>>>>> ae4aa50f4d70edf85bcea1a0dac5f7e22b93f9aa
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"


async def main():
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha")),
        asyncio.create_task(fetch_stock_price("Beta")),
        asyncio.create_task(fetch_stock_price("Gamma")),
    }

    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )

    for winner in done:
        print(f"{ctime()} Winner Result: {winner.result()}")

    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")

    for task in pending:
        task.cancel()


asyncio.run(main())