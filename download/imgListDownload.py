import traceback
from util.logUtil import download_log
from download import baseDownload


class ImgListDownload(baseDownload.Download):
    def __init__(self, headers=..., params="") -> None:
        super().__init__(headers=headers, params=params)

    def doDown(self, task):
        # 改成先下载到本地存储，下载成功后从本地上传到服务器，上传成功后，删除本地存储
        try:
            content = self.page_down(task.task_url)
            if not content:
                return False

        except:
            download_log.error(
                f'{task.site_name}  task_url: {task.task_url};   error:{str(traceback.format_exc())}'
            )
            return False
        return content