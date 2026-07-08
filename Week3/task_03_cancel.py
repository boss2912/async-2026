# Objective: Stop an ongoing execution prematurely by triggering a cancellation exception.
import asyncio
from time import ctime

async def background_loop():
    try:
        print(f"{ctime()} Worker: Starting long infinite process...")
        while True: #run ตลอดเวลา ทุกๆ 1 วินาที
            await asyncio.sleep(1)
            print(f"{ctime()} Worker: Still ticking...")
    except asyncio.CancelledError:
        # Injected when task.cancel() is executed at next aeait checkpoint
        print(f"{ctime()} Worker: Interrupted! Executing clean-up logic before exit...")

async def main():
    task = asyncio.create_task(background_loop())
    await asyncio.sleep(2.5) # Let the background task tick a few times
    
    print(f"{ctime()} Main: Changing plans, canceling the worker task now!")
    task.cancel() # Request cancellation
    await asyncio.sleep(0.1) # Yield execution windows to let worker run its except block

asyncio.run(main())