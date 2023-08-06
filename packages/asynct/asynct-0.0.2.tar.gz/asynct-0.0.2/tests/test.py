from ..asynct import make_asynct, Asynct
import time

@make_asynct
def x():
    time.sleep(1)
    return 'x'
@make_asynct
def y():
    time.sleep(2)
    return 'y'
# print('x')
print(Asynct.race(x(), y()).await_it())
# print('z')