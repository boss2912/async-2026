# Objective: Compare the structural and mechanical differences of both strategies in a racing scenario.
import asyncio
from time import ctime

async def runner(name, speed):
    await asyncio.sleep(speed)
    return f"{name} crossed line!"

async def main():
    # Case A: USing gather() -> We must wait for all items to finish to get the ordered list
    print(f"{ctime()} --- Starting gather() approach (Unified Aggregation) ---")
    all_finishes = await asyncio.gather(runner("A", 0.5), runner("B", 2.0))
    print(f"{ctime()} Gather output: {all_finishes}\n")
    
    # Case B: Using wait() -> We can decouple early as soon as a condition matches
    print(f"{ctime()} --- Starting wait() approach (State control / Racing) ---")
    active_tasks = {asyncio.create_task(runner("A", 0.5)), asyncio.create_task(runner("B", 2.0))}
    
    done, pending = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"{ctime()} Wait output: The winner of the race is -> {list(done)[0].result()}")
    
    # Clean up the loser task
    for t in pending:
        t.cancel()

asyncio.run(main())