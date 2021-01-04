import threading
from queue import Queue
import time

print_lock = threading.Lock()
q = Queue()


def dummy_function(item):
    """
    Wait 2 seconds and print the current thread name and the item
    :param item: value taken from the queue
    """
    time.sleep(5)
    with print_lock:
        print(threading.current_thread().name, '\t\t[{}]'.format(item))


def threader():
    """
    Take an item from the queue and exec the dummy function
    """
    while True:
        item_from_queue = q.get()  # Remove and return an item from the queue.
        dummy_function(item_from_queue)
        q.task_done()


if __name__ == '__main__':

    # This loop generate threads for the threader function
    # Simulate that we only have a limit of 10 threads
    for x in range(10):
        t = threading.Thread(target=threader)
        # will die when main thread dies
        t.daemon = True
        t.start()  # exec the threader function

    start = time.time()  # starting time

    # Add 50 items to the queue
    for y in range(50):
        q.put(y)

    q.join()  # will wait until the thread terminates

    print("Entire time took:", time.time() - start)
