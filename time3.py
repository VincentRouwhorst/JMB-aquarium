import sched, time
from time import gmtime, strftime

s = sched.scheduler(time.time, time.sleep)

def print_time(): 
    print("From print_time", strftime("%H:%M:%S", time.time()))

def print_some_times():
    print(time.time())
    s.enter(1, 1, print_time, ())
    s.enter(2, 1, print_time, ())
    s.enter(3, 1, print_time, ())
    s.enter(4, 1, print_time, ())
    s.enter(5, 1, print_time, ())
    s.run()
    print(time.time())


print_some_times()
#strftime("%H:%M:%S", gmtime())
