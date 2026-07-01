# Program 6: Creating a Concurrent Task
# Concept: Wrapping a coroutine inside asyncio.create_task() to schedule it to run in the background.
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
    
    print(f"{ctime()} -> Tasks Created, Now Awaiting Completion...")
    
    # Awaiting the completion of both tasks
    await task_a
    
    print(f"Total Operation Time: {time() - start_time:.2f} seconds")  # Will be around 2 seconds
    
if __name__ == "__main__":
    asyncio.run(main())  # Run the main coroutine
