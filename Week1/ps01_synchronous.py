from time import sleep, ctime, time, process_time
import os
import threading
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คนแบบซิงโครนัส
def make_coffee(customer_name):

    # ดึง PID และ Thread ID
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Thread Name: {thread_name}] "
        f"กำลังชงกาแฟให้ ลูกค้า {customer_name}..."
    )

    # งานคำนวณหนัก (CPU-bound)
    sum(i * i for i in range(1000000))

    # งานรอ (I/O-bound)
    sleep(5)

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Thread Name: {thread_name}] "
        f"ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!"
    )


def main():

    queue = ['A', 'B', 'C']

    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(
        f"{ctime()} | [Main PID: {main_pid}] "
        f"[Main TID: {main_tid}] "
        f"=== เริ่มระบบจำลองร้านกาแฟแบบ Synchronous ==="
    )

    start_time = time()           # เวลาจริง
    start_cpu = process_time()    # เวลา CPU

    # ทำงานทีละคน
    for customer in queue:
        make_coffee(customer)

    duration = time() - start_time
    cpu_duration = process_time() - start_cpu

    # ตรวจสอบ RAM
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)

    print("\n[สรุปผล Synchronous]")
    print(f"เวลาที่ใช้จริง (Wall Time): {duration:.2f} วินาที")
    print(f"เวลาที่ CPU ใช้จริง (CPU Time): {cpu_duration:.4f} วินาที")
    print(f"การใช้ RAM: {mem_mb:.2f} MB")


if __name__ == "__main__":
    main()