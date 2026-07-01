# Program 3: The Event Loop (asyncio.run)
# Concept: Using the Event Loop to actually execute a Coroutine Object.
import asyncio

async def greet():
    print("Hello from the Event Loop!")

if __name__ == "__main__":
    coro_obj = greet()  # Create a Coroutine Object
    
    # Use the Event Loop to execute the Coroutine Object
    asyncio.run(coro_obj)
