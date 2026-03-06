import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

fomatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

console_handler.setFormatter(fomatter)
file_handler.setFormatter(fomatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def timer(func2):
    @wraps(func2)
    def TimerWrapper(*args, **kwargs):
        """TimerWrapper Docstring"""
        print("start timer")
        start = time.time()
        func2(*args, **kwargs)
        end = time.time()
        logger.warning(f"Time taken: {end - start}")
    return TimerWrapper

def logging(func1):
    # func is available
    @wraps(func1)
    def LogWrapper(*args, **kwargs):
        """LogWrapper Docstring"""
        logger.warning("logging start")
        func1(*args, **kwargs)
        logger.warning("logging end")
    return LogWrapper

@timer
@logging
def hello(name  = "world"):
    """ The Docstring is Metadata too! """
    print("hello "+ name)
    print(hello.__name__)
    print(hello.__doc__)







@logging
@timer
def addition(a,b):
    return a + b

# hello = my_dec(hello)
hello("Andrew")

# print(addition(b=2,a=3))