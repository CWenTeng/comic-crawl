import threading
import time
from concurrent.futures import ThreadPoolExecutor
import traceback

import config
from download.imgDownload import ImgDownload
from util.logUtil import download_log, except_log
from cache import workQueue


# 图片
class ImgWork:
    # def __init__(self) -> None:
    #     self.executor = ThreadPoolExecutor(max_workers=config.IMG_DOWNLOAD_THREAD)

    def doCrawl(self, task):
        imgDownload = ImgDownload(headers=task.head)
        content = imgDownload.doDown(task)
        if not content:
            # 重试
            if task.retry < config.RETRY or config.RETRY == -1:
                task.retry += 1
                workQueue.put_queue("imgQueue", task)
                download_log.warning(f'放回队列重试; task_url:{task.imgUrl};  retry:{task.retry}')
            else:
                download_log.warning(f'重试失败;  task_url:{task.imgUrl};  retry:{task.retry}')

    def work_thread(self):
        try:
            while True:
                task = workQueue.get_queue("imgQueue")
                if task:
                    # self.executor.submit(self.doCrawl, task)
                    self.doCrawl(task)
                else:
                    time.sleep(10)
        except:
            except_log.error(
                f'task_url:{task.task_url};   error:{traceback.format_exc()}')

    def run(self):
        for i in range(config.IMG_DOWNLOAD_THREAD):
            t = threading.Thread(target=self.work_thread)
            t.daemon = True
            t.start()
