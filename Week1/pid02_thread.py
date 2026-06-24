from time import sleep, ctime, time
import threading
import os

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

    sleep(5)  # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาที

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
        f"=== เริ่มระบบจำลองร้านกาแฟแบบ Multi-Thread ==="
    )

    start_time = time()

    threads = []

    # สร้าง Thread สำหรับลูกค้าแต่ละคน
    for customer in queue:

        # ตั้งชื่อ Thread ตามชื่อลูกค้า
        t = threading.Thread(
            target=make_coffee,
            args=(customer,),
            name=f"Thread-{customer}"
        )

        threads.append(t)

        # เริ่มทำงานพร้อมกัน
        t.start()

    # รอให้ทุก Thread ทำงานเสร็จ
    for t in threads:
        t.join()

    duration = time() - start_time

    print(
        f"{ctime()} | ใช้เวลารวมทั้งหมด: {duration:.2f} วินาที"
    )


if __name__ == "__main__":
    main()