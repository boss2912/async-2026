from time import sleep, ctime, time
import multiprocessing
import threading
import os

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):

    # ดึง PID ของหน่วยประมวลผลนี้ (จะแยกกันเด็ดขาด)
    pid = os.getpid()

    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(
        f"{ctime()} | [PID: {pid}] "
        f"[TID: {thread_id}] "
        f"[Thread Name: {thread_name}] "
        f"กำลังชงกาแฟให้ ลูกค้า {customer_name}..."
    )

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
        f"=== เริ่มระบบจำลองร้านกาแฟแบบ Multi-processing ==="
    )

    start_time = time()

    processes = []

    # สร้าง Process แยก
    for customer in queue:

        p = multiprocessing.Process(
            target=make_coffee,
            args=(customer,)
        )

        processes.append(p)
        p.start()

    # รอให้ทุก Process เสร็จ
    for p in processes:
        p.join()

    duration = time() - start_time

    print(
        f"{ctime()} | ใช้เวลารวมทั้งหมด: {duration:.2f} วินาที"
    )


if __name__ == "__main__":
    main()