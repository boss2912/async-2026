from time import sleep, ctime, time
import multiprocessing

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน 
def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(2.0)
    print(f"{ctime()} | Coffee ready for {customer_name}!")

def main():
    queue = ['A', 'B', 'C']
    print(f"{ctime()} | === Multi-processing Coffee Machine ===")
    
    start_time = time()
    processes = []
    
    # โยนงานให้แต่ละ Process ทำพร้อมกัน
    for customer in queue:
        p = multiprocessing.Process(target=make_coffee, args=(customer,))
        processes.append(p)
        p.start()
        
    # รอให้ทุก Process ทำงานเสร็จก่อนสรุปเวลา
    for p in processes:
        p.join()
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

# สิ่งสำคัญที่สุดสำหรับ Multi-processing ใน Python: ต้องครอบด้วยบล็อกนี้เสมอ
if __name__ == "__main__":
    main()
    