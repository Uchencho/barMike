import time, asyncio

def task_that_takes_time():
    print("I got called at least")
    time.sleep(3)
    print("I just finished running after three seconds")
    return