# Program 2: The Coroutine Object
# Concept: Seeing that calling an async def function creates an "Object" but does not execute it yet.
import asyncio

async def greet():
    print("Hello!")

# Calling the coroutine function creates a "Coroutine Object"
coro_obj = greet()

# Notice that "Object" is created but the function is not executed yet.
print(type(coro_obj))  # Output: <class 'coroutine'>

coro_obj.close()  # Closing the coroutine object to clean up resources.