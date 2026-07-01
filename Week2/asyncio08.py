# Program 8: Task Interleaving (Context Switching)
# Concept: Watching a single thread switch back and forth between two different workflows using create_task.
import asyncio
from time import ctime

async def kitchen_crew():
    print(f"{ctime()} -> [Chef] puts noodle in boiling water...")
    await asyncio.sleep(1)  # Yields control while waiting
    print(f"{ctime()} -> [Chef] stretches the noodle!")
    
async def bar_crew():
    print(f"{ctime()} -> [Bar] starta grinding coffee bean...")
    await asyncio.sleep(1)  # Yields control while waiting
    print(f"{ctime()} -> [Bar] pours espresso shot!")
    
async def main():
    # Creating concurrent tasks for kitchen and bar crew
    task_kitchen = asyncio.create_task(kitchen_crew())
    task_bar = asyncio.create_task(bar_crew())
    
    print(f"{ctime()} -> Tasks Created, Now Awaiting Completion...")
    
    # Awaiting the completion of both tasks
    await task_kitchen
    await task_bar

if __name__ == "__main__":
    asyncio.run(main())  # Run the main coroutine