# from .fly_log import debug_print
from fly_log import debug_print as print, log_time 
import time

def test1():
    print("my fly log ") 

@log_time 
def test2():
    time.sleep(0.5) 


def dev_run():
    test1()
    test2()  


if __name__ == '__main__':
    dev_run()
