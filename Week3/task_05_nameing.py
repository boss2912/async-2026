# Objective: Label task objects explicitly to simplify logging and production tracking.
import asyncio
from time import ctime

async def background_worker():
    await asyncio.sleep(0.1)

async def main():
    task = asyncio.create_task(background_worker())
    
    # Default auto-generated name assigned by Python framework
    print(f"{ctime()} Initial Name: {task.get_name()}") # Expected: Task-2
    
    # Override
    task.set_name("Payment-Gateway-Validator")
    print(f"{ctime()} Updated Name: {task.get_name()}") # Expected: Payment-Gateway-Validator

asyncio.run(main())