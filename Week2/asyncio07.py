# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently and awaiting them individually without gather.
import asyncio
from time import time, ctime

async def cook_spaghetti(customer):
    print(f"{ctime()} -> Starting for Cooking for Customer {customer}...")
    await asyncio.sleep(1)  # Simulate a delay in cooking
    print(f"{ctime()} -> Finished Cooking for Customer {customer}!")
    
async def main():
    start_time = time()
    
    # Creating concurrent tasks for each customer
    task_a = asyncio.create_task(cook_spaghetti("A"))
    task_b = asyncio.create_task(cook_spaghetti("B"))
    
    print(f"{ctime()} -> Tasks Created, Now Awaiting Completion...")
    
    # Awaiting the completion of both tasks
    await task_a
    await task_b
    
    print(f"Total Operation Time: {time() - start_time:.2f} seconds")  # Will be around 2 seconds
    
if __name__ == "__main__":
    asyncio.run(main())  # Run the main coroutine

