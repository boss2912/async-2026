from time import ctime, time
import asyncio
import os
import threading

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):

    # 1. Process ID และ Thread ID
    pid = os.getpid()
    thread_id = threading.current_thread().native_id

    # 2. ข้อมูล Task ปัจจุบันของ asyncio
    current_task = asyncio.current_task()
    task_name = current_task.get_name()

    # 3. Unique ID ของ Task
    task_id = id(current_task)

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Async Task ID: {task_id}] "
        f"[Task Name: {task_name}] "
        f"กำลังชงกาแฟให้ ลูกค้า {customer_name}..."
    )

    # Non-blocking wait
    await asyncio.sleep(5)

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Async Task ID: {task_id}] "
        f"[Task Name: {task_name}] "
        f"ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!"
    )


async def main():

    queue = ['A', 'B', 'C']

    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(
        f"{ctime()} | [Main PID: {main_pid}] "
        f"[Main TID: {main_tid}] "
        f"=== เริ่มระบบจำลองร้านกาแฟแบบ asyncio ==="
    )

    start_time = time()

    tasks = []

    for customer in queue:

        coro = make_coffee(customer)

        task = asyncio.create_task(
            coro,
            name=f"Task-{customer}"
        )

        tasks.append(task)

    await asyncio.gather(*tasks)

    duration = time() - start_time

    print(
        f"{ctime()} | ใช้เวลารวมทั้งหมด: {duration:.2f} วินาที"
    )


if __name__ == "__main__":
    asyncio.run(main())