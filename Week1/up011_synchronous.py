from time import sleep, ctime, time

def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1.0)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1.0)
    print(f"{ctime()} | Coffee ready for {customer_name}!")
    # เรียกใช้ฟังก์ชันอัปเดตหน้าจอหลังจากชงเสร็จ
    update_cup_number(customer_name)

def main():
    queue = ['A', 'B', 'C']
    print(f"{ctime()} | === Synchronous Coffee Machine ===")
    
    start_time = time()
    
    # ทำงานทีละคิว (ลูกค้า 1 คนใช้เวลา 2 วินาที)
    for customer in queue:
        make_coffee(customer)
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

if __name__ == "__main__":
    main()