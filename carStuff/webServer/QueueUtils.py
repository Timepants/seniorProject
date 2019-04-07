from multiprocessing import Queue

def stopQueue(queue):
    while not queue.empty():
        queue.get() 
    for i in range(20):
        queue.put(False)

def startQueue(queue):
    while not queue.empty():
        queue.get() 
    queue.put(True)

def skipInQueue(queue):
    data = dict()
    while not queue.empty():
        data = queue.get()
    return data
