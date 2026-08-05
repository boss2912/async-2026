# from time import sleep, ctime, time

# # ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
# def make_coffee(customer_name):
#     print(f"{ctime()} | Making coffee for {customer_name}...")
#     sleep(2.0)
#     print(f"{ctime()} | Coffee ready for {customer_name}!")

# def main():
#     # คิวลูกค้า
#     queue = ['A', 'B', 'C']
#     print(f"{ctime()} | === Synchronous Coffee Machine ===")
    
#     start_time = time()
    
#     for customer in queue:
#         make_coffee(customer)
        
#     duration = time() - start_time
#     print(f"{ctime()} | Total time: {duration:.2f} seconds")

# # สั่งให้โปรแกรมทำงาน
# if __name__ == "__main__":
#     main()


# from time import ctime, time
# import asyncio
    
# async def welcome_customer(customer):
    
#     print(f"Welcome {ctime()} | [ต้อนรับ] สวัสดีคุณ {customer}")
#     await asyncio.sleep(1)
#     print(f"Goodbye {ctime()} | [ต้อนรับ] พาคุณ {customer}")
    
# async def serve_full_course(customer):
    
#     print(f"{ctime()} | [บริการ] รับออเดอร์คุณ {customer}")
#     await asyncio.sleep(1)
#     print(f"{ctime()} | [บริการ] ทำอาหารให้คุณ {customer}")
#     await asyncio.sleep(1)
#     print(f"{ctime()} | [บริการ] เสิร์ฟเครื่องดื่มให้คุณ {customer}")
#     await asyncio.sleep(1)
    
#     print(f"{ctime()} | [สำเร็จ] บริการคุณ {customer}")
    

# async def main():
    
#     start_time = time()
#     customers = ["A", "B", "C"]
#     tasks = []
    
#     for customer in customers:
#         await welcome_customer(customer)
    
#     taska = [serve_full_course(customer) for customer in customers]
#     await asyncio.gather(*taska)
    
    
#     print(f"{ctime()} total time: {time() - start_time:.2f} seconds")

# if __name__ == "__main__":
#     asyncio.run(main())
    
    
    
# from time import ctime, time
# import asyncio

# async def cook_mine_dish(dish_name, sec):
    
#     m = float(0.0)
    
#     print(f"{ctime()} | [เซฟของคาว] เเริ่มทำ {dish_name}...")
#     await asyncio.sleep(sec)
#     print(f"{ctime()} | [เซฟของคาว] ทำ {dish_name} เสร็จแล้ว")
    
#     m = float(250.0)
#     return m

# async def make_dessert(dessert_name, sec):
    
#     d = float(0.0)
    
#     print(f"{ctime()} | [เซฟของหวาน] เริ่มทำ {dessert_name}...")
#     await asyncio.sleep(sec)
#     print(f"{ctime()} | [เซฟของหวาน] ทำ {dessert_name} เสร็จแล้ว")
    
#     d = float(120.0)
#     return d

# async def main():
    
#     start_time = time()
    
#     K = asyncio.create_task(cook_mine_dish("สเต็ก", 4))
#     I = asyncio.create_task(make_dessert("ไอศกรีม", 2))
    
#     await K
#     await I
    
#     print(f"{ctime()} | [สำเร็จ] ทำอาหารเสร็จแล้ว")
    
#     print(f"{ctime()} | [สำเร็จ] รวมค่าใช้จ่ายทั้งหมด: {K.result() + I.result()} บาท")
    
#     print(f"{ctime()} | [สำเร็จ] รวมเวลาในการทำอาหารทั้งหมด: {time() - start_time:.2f} วินาที")
    
# if __name__ == "__main__":
#     asyncio.run(main())
    

from time import ctime, time
import asyncio

async def check_stock(item_name: str, count: int):
	await asyncio.sleep(0.5);
	
	if count <= 0:
		raise ValueError(f"สินค้า {item_name} หมดสต็อก!");
	else:
		return f"สินค้า {item_name} มีพร้อมส่ง {count} ชิ้น"
		
async def main():

	Check_Shirt = asyncio.create_task(check_stock("เสื้อ", 5))
	Check_Shirt.set_name("Check_Shirt")
	Check_Pants = asyncio.create_task(check_stock("กางเกง", 0))
	Check_Pants.set_name("Check_Pants")

	#p1
	# Check_Shirt = asyncio.create_task(check_stock("เสื้อ", 5))
	# Check_Pants = asyncio.create_task(check_stock("กางเกง", 0))
	
	await asyncio.sleep(1);
	
	#p2
	if Check_Shirt.exception():
		print(f"เกิดข้อผิดพลาด:{Check_Shirt.exception()}")
	else:
		print(f"ผลลัพธ์: {Check_Shirt.result()}")

	if Check_Pants.exception():
		print(f"เกิดข้อผิดพลาด:{Check_Pants.exception()}")
	else:
		print(f"ผลลัพธ์: {Check_Pants.result()}")
		
# if __name__ == "__main__":
	
asyncio.run(main())