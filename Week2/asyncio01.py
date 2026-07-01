# Program 1: The First Coroutine Function
# Concept: Understanding async def and how it differs from a normal function.
import asyncio

# A regular function uses the 'def' . An asynchronous function uses the 'async def' syntax.
# This defines a "Coroutine Function"
async def greet():
    print("Hello from Coroutine!")
    
print(type(greet))  # Output: <class 'function'>