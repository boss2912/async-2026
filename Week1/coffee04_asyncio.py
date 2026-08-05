from time import ctime, time
import asyncio

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    await asyncio.sleep(2.0) # คืนการควบคุมให้ Event Loop
    print(f"{ctime()} | Coffee ready for {customer_name}!")

async def main():
    queue = ['A', 'B', 'C']
    print(f"{ctime()} | === Asyncio Coffee Machine ===")
    
    start_time = time()
    
    # ห่อ Coroutine เข้าด้วยกันและรันแบบ Concurrent
    tasks = [make_coffee(customer) for customer in queue]
    await asyncio.gather(*tasks)
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

# สั่งให้ระบบ Async เริ่มทำงาน
if __name__ == "__main__":
    # ใช้ asyncio.run เพื่อเปิด Event Loop หลักของโปรแกรม
    asyncio.run(main())