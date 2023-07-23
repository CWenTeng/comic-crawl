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
    title_num_list = []
    head = {
    }
    # 漫画列表
    lis = html.xpath("//div[@class='stui-pannel_bd col-pd clearfix']/ul/li")
    try:
        book_title = html.xpath("//div[@class='stui-content__detail']/h1[@class='title']/text()")[0]
    except:
        book_title = str(time.time())
    try:
        # 创建漫画书目录
        book_filePath = '/'.join([path, book_title])
        if not os.path.exists(book_filePath):
            os.mkdir(book_filePath)
    except:
        parse_log.error(f'baiman book_title:{book_title};     book_url:{task.task_url};     error:{traceback.format_exc()}')
        raise
    # 集数
    crawl_num = task.crawl_num
    title_id = ''
    if lis:
        try:
            fistLi = lis[0]
            lastLi = lis[len(lis) - 1]
            fistUrl = fistLi.xpath('./a/@href')[0]
            lastUrl = lastLi.xpath('./a/@href')[0]
            r = re.search(r'\d+(?=.html)', fistUrl)
            fist_id = int(r.group())
            r = re.search(r'\d+(?=.html)', lastUrl)
            last_id = int(r.group())
            if fist_id > last_id:
                parse_log.debug('baiman 翻转列表  fist_id:%s;  last_id:%s;' %
                                (fist_id, last_id))
                lis = lis[::-1]
        except:
            parse_log.error(f'baiman 列表排序失败    baiman book_title:{book_title};     book_url:{task.task_url};     error:{traceback.format_exc()}')
        else:
            parse_log.info('baiman  book_title:%s;  size:%d' %
                        (book_title, len(lis)))

    for li in lis:
        try:
            url = li.xpath("./a/@href")[0]
            # if 'http' not in url:
            #     url = 'https://www.36mh.net' + url
            title = li.xpath("./a/text()")
            if title:
                title = title[0]
            # 匹配集数
            title_num = ''
            r = re.search(r'(?<=第)\d+(?=话)',title)
            # r = re.search(r'\d+(?=.html)', url)
            try:
                # title_num = r.group()
                title_id = r.group()
            except:
                # try:
                #     r = re.search(r'\d{1,3}',title)
                #     title_num = r.group()
                # except:
                #     parse_log.error('title:%s; error:%s'%(title,str(traceback.format_exc())))
                parse_log.error('title:%s; title_id:%s; error:%s' %
                                (title, title_id, str(traceback.format_exc())))
                continue
            # 增量抓取，过滤历史数据
            if task.crawl_flag:
                if int(title_id) <= int(task.crawl_flag):
                    parse_log.debug(
                        'baiman 增量过滤  chapter:%s;  title:%s;  title_id:%s' %
                        (url, title, title_id))
                    continue
            # # 补全集数编号位数
            # while title_num:
            #     if len(title_num)>=4:
            #         break
            #     title_num = '0'+title_num
            # if(title_num in title_num_list):
            #     continue
            if (title_id in title_num_list):
                continue
            # title_num_list.append(title_num)
            title_num_list.append(title_id)
            # 格式化
            title = utils.formatting(title)
            # parse_log.info('title: %s'%(title))
            # 补全集数编号位数
            title_num = str(crawl_num)
            while title_num:
                if len(title_num) >= 4:
                    break
                title_num = '0' + title_num
            title = title_num + '_' + title
            parse_log.info('baiman chapter:%s;  title:%s;  title_num:%s' %
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
            # workQueue.put_queue("imgListQueue",imglisttask)
        except:
            parse_log.error('baiman title:%s; error:%s' %
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
        parse_log.error('baiman title:%s; SQL error:%s' %
                        (title, str(traceback.format_exc())))
    return imgListTaskList


# baiman 图片列表
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
        parse_log.error('baiman  book_title:%s; error:%s' % (book_title, str(traceback.format_exc())))
        raise
    chapterPath = ""
    path = config.PATH
    head = {}
    # 图片编号
    num = 1
    # 匹配图片列表
    try:
        r = re.search("(?<=var txt_url=\").*(?=\")", html)
        imgListUrl = r.group()
        imgListContent = Download().page_down(imgListUrl)
        imgListHtml = etree.HTML(imgListContent)
        imgList = imgListHtml.xpath("//p/img/@src")
        
        parse_log.info('baiman  size:%d;  imgList:%s' % (len(imgList), imgList))
    except:
        parse_log.error('baiman Task url:%s;   Regular rule:%s;  error:%s' % (task.task_url, str(traceback.format_exc())))
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
            parse_log.info('baiman  chapter:%s;  img_filePath:%s;  img_num:%s' % (imgUrl, img_filePath, img_num))
        except:
            parse_log.warning('baiman  img_filePath:%s; warn:%s' % (img_filePath, str(traceback.format_exc())))
        else:
            # 入章节列表队列
            imgName = img_num + '.jpg'
            imgtask = ImgTask(imgUrl=imgUrl, task_id=task.task_id, purl=task.task_url,
                                      filePath=img_filePath, imgName=imgName, head=head, site_name=task.site_name)
            imgTaskList.append(imgtask)
        num += 1
    
    return imgTaskList
    # (?<=;var chapterImages = ).*]