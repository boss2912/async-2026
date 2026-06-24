from time import sleep, ctime, time, process_time
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):

    # ดึง PID ของระบบ (จะเหมือนกันทุก Thread)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Thread Name: {thread_name}] "
        f"กำลังชงกาแฟให้ ลูกค้า {customer_name}..."
    )

    # งานคำนวณเล็กน้อย (CPU-bound)
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
        f"=== เริ่มระบบจำลองตู้กาแฟแบบ Multi-Thread ==="
    )

    start_time = time()
    start_cpu = process_time()

    threads = []

    # สร้าง Thread สำหรับลูกค้าแต่ละคน
    for customer in queue:

        # ตั้งชื่อ Thread เพื่อให้อ่านง่าย
        t = threading.Thread(
            target=make_coffee,
            args=(customer,),
            name=f"Thread-{customer}"
        )

        threads.append(t)
        t.start()

    # รอให้ทุก Thread ทำงานเสร็จ
    for t in threads:
        t.join()

    duration = time() - start_time
    cpu_duration = process_time() - start_cpu

    # วัด RAM
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)

    print("\n[สรุปผล Multi-Thread]")
    print(f"เวลาที่ใช้จริง (Wall Time): {duration:.2f} วินาที")
    print(f"เวลาที่ CPU ใช้จริง (CPU Time): {cpu_duration:.4f} วินาที")
    print(f"การใช้ RAM: {mem_mb:.2f} MB")


if __name__ == "__main__":
    main()