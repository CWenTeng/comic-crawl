'''
图片任务
'''


class ImgTask:
    def __init__(self, imgUrl, task_id, filePath, imgName, purl='', head={}, site_name=''):
        self.purl = purl
        self.imgUrl = imgUrl
        self.filePath = filePath
        self.imgName = imgName
        self.head = head
        self.retry = 0
        self.site_name = site_name
        self.task_id = task_id
