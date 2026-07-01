# # Program 9: Dynamically Tracking Tasks in a List
# # Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.
# import asyncio
# from asyncio import tasks
# from time import time, ctime

# async def serve_customer(name):
#     print(f"{ctime()} -> Handling customer {name}")
#     await asyncio.sleep(1)  # Simulate a delay in serving the customer
#     print(f"{ctime()} -> Serving customer {name}!")
    
# async def main():
#     start_time = time()
#     customers = ["A", "B", "C", "D"]
#     task_list = []
   
#     # Dynamically creating tasks for each customer and appending them to the list
#     for name in customers:
#         task = asyncio.create_task(serve_customer(name))
#         task_list.append(task)
        
    
        
#     print(f"{ctime()} -> Tasks Created, Now Awaiting Completion...")
    
#     # Awaiting the completion of all tasks
#     await asyncio.gather(*task_list)
    
#     print(f"Total Operation Time: {time() - start_time:.2f} seconds")  # Will be around 1 second
    
# if __name__ == "__main__":
#     asyncio.run(main())  # Run the main coroutine

# Program 9: Dynamically Tracking Tasks in a List
# Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.

import asyncio
from time import time, ctime

async def serve_customer(name):
    print(f"{ctime()} | Serving customer: {name}")
    await asyncio.sleep(1)  # Simulate time taken to serve customer
    print(f"{ctime()} | Finished serving customer: {name}")
       
async def main():
    start = time()
    
    # List to hold the tasks
    tasks = []
    
    # Dynamically create tasks for multiple customers
    for customer in ["Alice", "Bob", "Charlie", "David"]:
        task = asyncio.create_task(serve_customer(customer))
        tasks.append(task)  # Append the task to the list
    
    # Wait for all tasks to complete
    #await asyncio.gather(*tasks)
    for task in tasks:
        await task  # Await each task to ensure they complete
    
    print(f"Total Time: {time() - start:.2f} seconds")
    
if __name__ == "__main__":
    asyncio.run(main())  # Run the main coroutine using the event loop