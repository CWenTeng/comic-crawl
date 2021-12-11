from queue import Queue
from util.logUtil import queue_log


def init():
    global WORK_QUEUE_DICT

    IMG_QUEUE = Queue()
    CHAPTER_LIST_QUEUE = Queue()
    IMG_LIST_QUEUE = Queue()

    WORK_QUEUE_DICT = {
        "chapterListQueue": CHAPTER_LIST_QUEUE,
        "imgListQueue": IMG_LIST_QUEUE,
        "imgQueue": IMG_QUEUE,
    }


def put_queue(queueName, task):
    WORK_QUEUE_DICT[queueName].put(task)


def get_queue(queueName):
    if WORK_QUEUE_DICT[queueName].empty():
        queue_log.info(f"{queueName} size: empty")
        return None
    queue_log.info(f"{queueName} size: {WORK_QUEUE_DICT[queueName].qsize()}")
    return WORK_QUEUE_DICT[queueName].get()
        
