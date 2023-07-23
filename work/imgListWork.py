import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import config
from download.imgListDownload import ImgListDownload
from util.logUtil import download_log, parse_log, except_log
from cache import workQueue, pluginCache


# 图片列表
class ImgListWork:
    # def __init__(self) -> None:
    #     self.executor = ThreadPoolExecutor(max_workers=config.IMG_LIST_THREAD)

    def doCrawl(self, task):
        imgListDownload = ImgListDownload(headers=task.head)
        content = imgListDownload.doDown(task)
        if content:
            try:
                plugin = pluginCache.get_plugin(task.site_name)
                functionName = "img_list_parse"
                if hasattr(plugin, functionName):
                    pluginFunction = getattr(plugin,functionName)
                    subtaskList = pluginFunction(content, task)
                    # subtaskList = plugin.img_list_parse(content, task)
                    while(workQueue.get_size("imgQueue")>1000):
                        time.sleep(1)
                    
                    for subtask in subtaskList:
                        workQueue.put_queue("imgQueue", subtask)
                    # parseFunction = getattr(plugin, functionName)
                    # parseFunction(content, task)
                else:
                    parse_log.error(f"Can't find {task.site_name}.{functionName}() function")
            except:
                parse_log.error(f"Can't find {task.site_name} plugin;   {traceback.format_exc()}")
            # # 解析图片列表
            # # 反射实现(解析函数命名规则 "imgListParse_" + site_name)
            # functionName = "imgListParse_" + task.site_name
            # if hasattr(imgListParse, functionName):
            #     parseFunction = getattr(imgListParse, functionName)
            #     parseFunction(content, task)
            # else:
            #     parse_log.error(f"Can't find {functionName} function")

        else:
            if task.retry < config.RETRY or config.RETRY == -1:
                task.retry += 1
                workQueue.put_queue("imgListQueue", task)
                download_log.warning(f'{task.site_name} 放回队列重试; task_url:{task.task_url};  retry:{task.retry}')
                return False
            else:
                download_log.warning(f'{task.site_name} 重试失败; task_url:{task.task_url};  retry:{task.retry}')
                return False

    def work_thread(self):
        while True:
            try:
                task = workQueue.get_queue("imgListQueue")
                if task:
                    # self.executor.submit(self.doCrawl, task)
                    self.doCrawl(task)
                else:
                    time.sleep(10)
            except:
                except_log.error(
                    f'task_url:{task.task_url};   error:{traceback.format_exc()}'
               )
        # with ThreadPoolExecutor(max_workers=config.IMG_LIST_THREAD) as executor:
        #     while True:
        #         try:
        #             task = workQueue.get_queue("imgListQueue")
        #             if task:
        #                 executor.submit(self.doCrawl, task)
        #                 # self.doCrawl(task)
        #             else:
        #                 time.sleep(10)
        #         except:
        #             except_log.error(
        #                 f'task_url:{task.task_url};   error:{traceback.format_exc()}'
        #             )

    def run(self):
        for i in range(config.IMG_LIST_THREAD):
            t = threading.Thread(target=self.work_thread)
            t.daemon = True
            t.start()
