# Objective: Learn how to query the lifecycle status of a task object.
#ตรวจสอบ Life-Cycle ของ Task Object
import asyncio
from time import ctime

async def short_job():
    await asyncio.sleep(1)
    return "Success"

async def main():
    task = asyncio.create_task(short_job())
    
    # Inspect status immediately while it is still running
    # เช็คการทำงานของ Task ขณะกำลังทำงานอยู่
    print(f"{ctime()} Is task done? {task.done()}")          # Expected: False
    print(f"{ctime()} Is task canceled? {task.cancelled()}")  # Expected: False #เริ่มเอา Task ไปเข้า event loop
    
    await task # รอให้ Task ทำงานเสร็จ
    # Inspect status again after it finishes
    # เช็คการทำงานของ Task หลังจากทำงานเสร็จแล้ว
    print(f"{ctime()} Is task done now? {task.done()}")      # Expected: True #ทำงานเสร็จแล้ว
    print(f"{ctime()} Is task canceled now? {task.cancelled()}") # Expected: False #ไม่ถูกยกเลิก

asyncio.run(main())