import time

start = time.time()


def timer_start():
    print("-----------------------------------------------")
    start = time.time()
    return start


def timer_end(start):
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print("-----------------------------------------------")
