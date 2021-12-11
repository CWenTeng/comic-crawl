'''
章节列表任务
图片列表任务
'''


class ImgListTask:
    def __init__(self, task_url, task_id, purl='', book_title='', title='', head={}, site_name=''):
        # 图片列表 URL
        self.task_url = task_url
        self.purl = purl
        # 书名
        self.book_title = book_title
        # 章节名
        self.title = title
        # self.filePath = filePath
        self.type = type
        self.retry = 0
        # 站点名
        self.site_name = site_name
        self.head = head
        self.task_id = task_id
