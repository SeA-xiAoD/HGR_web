from multiprocessing import Queue

def _init():
    global _global_queue
    _global_queue = Queue(maxsize=0)

def put_into_queue(value):
    _global_queue.put(value)

def get_from_queue():
    try:
        return _global_queue.get()
    except Exception as e:
        return None

def get_queue_remainder():
    return _global_queue.qsize()

_init()