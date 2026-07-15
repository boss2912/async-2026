    # foodcourt_05_mix_concepts.py
    import asyncio
    from time import time, ctime
    from food_utils import send_order_to_kitchen


    async def main():
        MY_STUDENT_ID = "6710301006"

        print(f"{ctime()} | --- [Task 5] Advanced Practice: Mixing concepts together ---")
        start_time = time()

        # 1. Noodle: order แบบปกติ ไม่มีเพดานเวลา (cook จริง 1.5s)
        task_noodle = asyncio.create_task(
            send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
        )

        # 2. Chicken Rice: ห่อด้วย wait_for (เพดาน 1.0s) ก่อน แล้วค่อยห่อด้วย create_task อีกชั้น
        #    ซ้อนกล่อง: create_task( wait_for( coroutine, timeout ) )
        task_chicken = asyncio.create_task(
            asyncio.wait_for(
                send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Mixed"),
                timeout=1.0
            )
        )

        # 3. รวมทั้งสอง task เข้า gather เดียวกัน
        #    return_exceptions=True กันไว้ เผื่อ chicken หลุดเพดานเวลาจริง (network จริงอาจช้ากว่า mock)
        results = await asyncio.gather(task_noodle, task_chicken, return_exceptions=True)

        noodle_result, chicken_result = results
        dishes_received = 0
        failures = []

        for name, r in [("Noodle", noodle_result), ("Chicken Rice", chicken_result)]:
            if isinstance(r, asyncio.TimeoutError):
                failures.append(name)
            elif isinstance(r, Exception):
                failures.append(name)
            else:
                dishes_received += 1

        if not failures:
            print(
                f"{ctime()} | Success: All food served on time! "
                f"Received {dishes_received} dishes."
            )
        else:
            print(
                f"{ctime()} | Partial success: Received {dishes_received} dish(es), "
                f"but timed out on: {', '.join(failures)}"
            )

        print(f"{ctime()} | Total elapsed time: {time() - start_time:.2f} seconds.")


    if __name__ == "__main__":
        asyncio.run(main())