from multiprocessing import Queue

def _init():
    global _global_queue
    global _switch
    _global_queue = Queue(maxsize=0)
    _switch = False

def put_into_queue(value):
    global _global_queue
    _global_queue.put(value)

def get_from_queue():
    global _global_queue
    try:
        return _global_queue.get()
    except Exception as e:
        return None

def get_queue_remainder():
    global _global_queue
    return _global_queue.qsize()

def store_on_switch():
    global _switch
    _switch = True

def store_off_switch():
    global _switch
    _switch = False

def get_switch():
    global _switch
    return _switch

_init()