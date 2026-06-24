from time import sleep, ctime, time, process_time
import multiprocessing
import threading
import os
import psutil


# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name, result_queue):

    # ดึง PID ของหน่วยประมวลผลนี้ (ซึ่งจะแยกกันเด็ดขาด)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Thread Name: {thread_name}] "
        f"กำลังชงกาแฟให้ ลูกค้า {customer_name}..."
    )

    start_cpu = process_time()

    # จำลองงานคำนวณ (CPU-bound)
    sum(i * i for i in range(1000000))

    # งานรอ (I/O-bound)
    sleep(5)

    cpu_duration = process_time() - start_cpu

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Thread Name: {thread_name}] "
        f"ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!"
    )

    # ส่งค่าการใช้ RAM และ CPU กลับไปให้ Main Process
    process = psutil.Process(pid)
    mem_mb = process.memory_info().rss / (1024 * 1024)

    result_queue.put((mem_mb, cpu_duration))


def main():

    queue = ['A', 'B', 'C']

    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(
        f"{ctime()} | [Main PID: {main_pid}] "
        f"[Main TID: {main_tid}] "
        f"=== เริ่มระบบจำลองตู้กาแฟแบบ Multi-processing ==="
    )

    start_time = time()
    main_start_cpu = process_time()

    result_queue = multiprocessing.Queue()

    processes = []

    # สร้าง Process ใหม่แยกจากกัน
    for customer in queue:

        p = multiprocessing.Process(
            target=make_coffee,
            args=(customer, result_queue)
        )

        processes.append(p)
        p.start()

    # รวบรวมข้อมูลจาก Child Process
    child_memories = []
    child_cpu_times = []

    for _ in queue:
        mem, cpu_t = result_queue.get()
        child_memories.append(mem)
        child_cpu_times.append(cpu_t)

    # รอทุก Process จบ
    for p in processes:
        p.join()

    duration = time() - start_time

    # RAM ของ Main Process
    main_process = psutil.Process(os.getpid())
    main_mem = main_process.memory_info().rss / (1024 * 1024)

    total_memory = main_mem + sum(child_memories)
    total_cpu_time = (process_time() - main_start_cpu) + sum(child_cpu_times)

    print("\n[สรุปผล Multi-processing]")
    print(f"เวลาที่ใช้จริง (Wall Time): {duration:.2f} วินาที")
    print(f"เวลารวมที่ CPU ทำงาน (Total CPU Time): {total_cpu_time:.4f} วินาที")
    print(
        f"การใช้ Memory (RAM) รวมทุก Process: "
        f"{total_memory:.2f} MB "
        f"(Main: {main_mem:.2f} MB + ย่อย: {sum(child_memories):.2f} MB)"
    )


if __name__ == "__main__":
    main()