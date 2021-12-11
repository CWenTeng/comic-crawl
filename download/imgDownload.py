import traceback
from download import baseDownload
from util.logUtil import download_log


class ImgDownload(baseDownload.Download):
    def __init__(self, headers=..., params="") -> None:
        super().__init__(headers=headers, params=params)

    def doDown(self, task):
        imgPath = '/'.join([task.filePath, task.imgName])

        try:
            # 图片url,主页url,图片页数
            # 下载图片
            if self.file_download(task.imgUrl, imgPath):
                # 上传
                return True
        except:
            download_log.error(
                f'imgUrl:{task.imgUrl};  retry:{task.retry}  error:{traceback.format_exc()}'
            )
        return False
