x = 0
y = 0
def foo(bar, baz):
    global x
    for i in range(20):
        baz.acquire()
        x += 1
        baz.release()
        print ('foo-y',y)
    return 'foo' + str(x)

def bar(bar, baz):
    global y

    for i in range(20):
        baz.acquire()
        y += 1
        baz.release()
        print ('bar-x',x)
    return 'bar' + str(y)

from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
pool = ThreadPool(processes=2)
lock = Lock()
async_result = pool.apply_async(foo, ('world', lock)) # tuple of args for foo
async_result2 = pool.apply_async(bar, ('world', lock)) # tuple of args for foo
# do some other stuff in the main process


return_val = async_result.get()  # get the return value from your function.

return_val2 = async_result2.get()  # get the return value from your function.

print(return_val)
print(return_val2)