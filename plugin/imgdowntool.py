from task.imgListTask import ImgListTask
from util.logUtil import parse_log
import traceback
import config
from lxml import etree
import re
import os
from task.imgTask import ImgTask
from download.baseDownload import Download
import time
from util import utils, sqlUtils


def chapter_list_parse(html, task):
    imgListTaskList = []
    html = etree.HTML(html)
    path = config.PATH
    head = {
    }
    # 漫画列表
    try:
        book_title = html.xpath("//title/text()")[0]
    except:
        book_title = str(time.time())
    try:
        # 创建漫画书目录
        book_filePath = '/'.join([path, book_title])
        if not os.path.exists(book_filePath):
            os.mkdir(book_filePath)
    except:
        parse_log.error(f'imgdowntool book_title:{book_title};     book_url:{task.task_url};     error:{traceback.format_exc()}')
        raise
    # 集数
    crawl_num = task.crawl_num
    title_id = 1
    
    try:
        url = task.task_url
        title = html.xpath("//title/text()")
        if title:
            title = title[0]
        # 匹配集数
        title_num = ''
        # 格式化
        title = utils.formatting(title)
        # 补全集数编号位数
        title_num = str(crawl_num)
        while title_num:
            if len(title_num) >= 4:
                break
            title_num = '0' + title_num
        title = title_num + '_' + title
        parse_log.info('imgdowntool chapter:%s;  title:%s;  title_num:%s' %
                        (url, title, title_num))
        # 入章节列表队列
        imglisttask = ImgListTask(task_url=url,
                                    task_id=task.task_id,
                                    purl=task.task_url,
                                    book_title=book_title,
                                    title=title,
                                    head=head,
                                    site_name=task.site_name)
        imgListTaskList.append(imglisttask)
    except:
        parse_log.error('imgdowntool title:%s; error:%s' %
                        (title, str(traceback.format_exc())))
    crawl_num += 1

    # 入库最后一集 title_id，下次从该 title_id 开始抓取
    # 入库集数 title_num ，下次从该 title_num 开始计数

    try:
        if task.crawl_flag:
            if int(title_id) <= int(task.crawl_flag):
                title_id = int(task.crawl_flag)
    except:
        parse_log.warning(f"title_id:{title_id}  crawl_flag:{task.crawl_flag}")
        title_id = int(task.crawl_flag)

    sql = f"""
    UPDATE crawl_task 
    SET crawl_flag = {title_id}, crawl_num = {crawl_num} 
    WHERE id = {task.task_id}
    """
    try:
        sqlUtils.exeSql(sql)
    except:
        parse_log.error('imgdowntool title:%s; SQL error:%s' %
                        (title, str(traceback.format_exc())))
    return imgListTaskList


# imgdowntool 图片列表
def img_list_parse(html, task):
    imgTaskList = []
    try:
        # 创建漫画书目录
        path = config.PATH
        book_title = task.book_title
        title = task.title
        img_filePath = '/'.join([path, book_title, title])
        if not os.path.exists(img_filePath):
            os.mkdir(img_filePath)
    except:
        parse_log.error('imgdowntool  book_title:%s; error:%s' % (book_title, str(traceback.format_exc())))
        raise
    chapterPath = ""
    path = config.PATH
    head = {}
    # 图片编号
    num = 1
    # 匹配图片列表
    try:
        imgList = html.xpath("//p/img/@data-src")
        
        parse_log.info('imgdowntool  size:%d;  imgList:%s' % (len(imgList), imgList))
    except:
        parse_log.error('imgdowntool Task url:%s;   Regular rule:%s;  error:%s' % (task.task_url, str(traceback.format_exc())))
        raise

    for img in imgList:
        try:
            # 格式化链接特殊字符
            imgUrl = img.replace('\/','/')
            img_num = str(num)

            # 补全集数编号位数
            while img_num:
                if len(img_num) >= 3:
                    break
                img_num = '0' + img_num
            parse_log.info('imgdowntool  chapter:%s;  img_filePath:%s;  img_num:%s' % (imgUrl, img_filePath, img_num))
        except:
            parse_log.warning('imgdowntool  img_filePath:%s; warn:%s' % (img_filePath, str(traceback.format_exc())))
        else:
            # 入章节列表队列
            imgName = img_num + '.jpg'
            imgtask = ImgTask(imgUrl=imgUrl, task_id=task.task_id, purl=task.task_url,
                                      filePath=img_filePath, imgName=imgName, head=head, site_name=task.site_name)
            imgTaskList.append(imgtask)
        num += 1
    
    return imgTaskList
    # (?<=;var chapterImages = ).*]