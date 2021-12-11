'''
章节列表任务
'''


class ChapterListTask:
    def __init__(self, task_url, task_id, purl='', head={}, crawl_flag='', crawl_num=0, site_name=''):
        # 图片列表 URL
        self.task_url = task_url
        # 任务类型
        self.head = head
        self.retry = 0
        # 周期任务标识
        self.crawl_flag = crawl_flag
        # 集数计数
        self.crawl_num = crawl_num
        # 站点名
        self.site_name = site_name
        self.purl = purl
        self.task_id = task_id
