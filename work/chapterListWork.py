import threading
from concurrent.futures import ThreadPoolExecutor
import time
import traceback

import config
from download.chapterListDownload import ChapterListDownload
from util.logUtil import download_log, parse_log, except_log
from cache import workQueue, pluginCache
# from parse import chapterListParse


class ChapterListWork:
    # def __init__(self) -> None:
    #     self.executor = ThreadPoolExecutor(max_workers=config.CHAPTER_LIST_THREAD)

    def doCrawl(self, task):
        chapterListDownload = ChapterListDownload(headers=task.head)
        content = chapterListDownload.doDown(task)
        if content:
            try:
                # 解析漫画列表
                # 反射实现(解析函数命名规则 "chapterListParse_" + site_name)
                plugin = pluginCache.get_plugin(task.site_name)
                functionName = "chapter_list_parse"
                if hasattr(plugin, functionName):
                    parseFunction = getattr(plugin, functionName)
                    subtaskList = parseFunction(content, task)
                    while(workQueue.get_size("imgListQueue")>1000):
                        time.sleep(1)
                    for subtask in subtaskList:
                        workQueue.put_queue("imgListQueue",subtask)
                else:
                    parse_log.error(f"Can't find {task.site_name}.{functionName}() function")
            except:
                parse_log.error(f"Can't find {task.site_name} plugin;   {traceback.format_exc()}")
            

        else:
            if task.retry < config.RETRY or config.RETRY == -1:
                task.retry += 1
                workQueue.put_queue("chapterListQueue", task)
                download_log.warning(f'{task.site_name} 放回队列重试;  task_url:{task.task_url};  retry:{task.retry}')
                return False
            else:
                download_log.warning(f'{task.site_name} 重试失败;  task_url:{task.task_url};  retry:{task.retry}')
                return False

    # 章节列表
    def work_thread(self):
        while True:
            try:
                task = workQueue.get_queue("chapterListQueue")
                if task:
                    # self.executor.submit(self.doCrawl, task)
                    self.doCrawl(task)
                else:
                    time.sleep(10)
            except:
                except_log.error(
                    f'task_url:{task.task_url};   error:{traceback.format_exc()}'
                )

        # with ThreadPoolExecutor(max_workers=config.CHAPTER_LIST_THREAD) as executor:
        #     while True:
        #         try:
        #             task = workQueue.get_queue("chapterListQueue")
        #             if task:
        #                 executor.submit(self.doCrawl,task)
        #                 # self.executor.submit(self.doCrawl, task)
        #                 # self.doCrawl(task)
        #             else:
        #                 time.sleep(10)
        #         except:
        #             except_log.error(
        #                 f'task_url:{task.task_url};   error:{traceback.format_exc()}'
        #             )

    def run(self):
        for i in range(config.CHAPTER_LIST_THREAD):
            t = threading.Thread(target=self.work_thread)
            t.daemon = True
            t.start()
