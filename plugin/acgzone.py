from task.imgListTask import ImgListTask
from util.logUtil import parse_log
import traceback
import config
from lxml import etree
import re
import os
from task.imgTask import ImgTask
import time
from util import utils, sqlUtils


def chapter_list_parse(html, task):
    imgListTaskList = []
    html = etree.HTML(html)
    path = config.PATH
    title_num_list = []
    head = {
        'referer': 'https://www.acgzone.net/',
    }
    # 漫画列表
    lis = html.xpath("//ul[@id='chapter-list-3']/li")
    if not lis:
        lis = html.xpath("//ul[@id='chapter-list-1']/li")
    try:
        book_title = html.xpath("//div[@id='comicName']/text()")
        if book_title:
            book_title = book_title[0]
        else:
            book_title = html.xpath("//h1/text()")[0]

    except:
        book_title = str(time.time())
    try:
        # 创建漫画书目录
        book_filePath = '/'.join([path, book_title])
        if not os.path.exists(book_filePath):
            os.mkdir(book_filePath)
    except:
        parse_log.error('acgzone book_title:%s; error:%s' %
                        (book_title, str(traceback.format_exc())))
        raise
    # 集数
    crawl_num = task.crawl_num
    # 尝试排序
    try:
        fistLi = lis[0]
        lastLi = lis[len(lis) - 1]
        if 'html' not in fistLi.xpath('./a/@href')[0]:
            lis.remove(fistLi)
            fistLi = lis[0]
        if 'html' not in lastLi.xpath('./a/@href')[0]:
            lis.remove(lastLi)
            lastLi = lis[len(lis) - 1]
        fistUrl = fistLi.xpath('./a/@href')[0]
        lastUrl = lastLi.xpath('./a/@href')[0]
        r = re.search(r'\d+(?=.html)', fistUrl)
        fist_id = int(r.group())
        r = re.search(r'\d+(?=.html)', lastUrl)
        last_id = int(r.group())
        if fist_id > last_id:
            parse_log.debug(f'{task.site_name} 翻转列表  fist_id:{fist_id};  last_id:{last_id};')
            lis = lis[::-1]
            lis = lis.sort()
    except:
        parse_log.error(f'{task.site_name} 列表排序失败   book_title:{book_title}; error:{str(traceback.format_exc())}')
    else:
        parse_log.info(f'{task.site_name}  book_title:{book_title};  size:{len(lis)}')

    for li in lis:
        try:
            url = li.xpath("./a/@href")[0]
            if 'http' not in url:
                url = 'https://www.acgzone.net' + url
            title = li.xpath("./a/span/text()")
            if title:
                title = title[0]
            # 匹配集数
            title_num = ''
            title_id = ''
            r = re.search(r'\d+(?=.html)', url)
            try:
                title_id = r.group()
            except:
                parse_log.error(
                    f'{task.site_name}  title:{title}; title_id:{title_id}; error:{str(traceback.format_exc())}'
                )
            # 增量抓取，过滤历史数据
            if task.crawl_flag:
                if int(title_id) <= int(task.crawl_flag):
                    parse_log.debug(
                        f'{task.site_name} 增量过滤  chapter:{url};  title:{title};  title_id:{title_id}'
                    )
                    continue
            if (title_id in title_num_list):
                continue
            title_num_list.append(title_id)
            # 格式化
            title = utils.formatting(title)
            # 补全集数编号位数
            title_num = str(crawl_num)
            while title_num:
                if len(title_num) >= 4:
                    break
                title_num = '0' + title_num
            title = title_num + '_' + title
            parse_log.info(f'{task.site_name} chapter:{url};  title:{title};  title_num:{title_num}')
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
            parse_log.error(f'{task.site_name} title:{title}; error:{str(traceback.format_exc())}')
        crawl_num += 1

    # 入库最后一集 title_id，下次从该 title_id 开始抓取
    # 入库集数 title_num ，下次从该 title_num 开始计数
    sql = f"""UPDATE crawl_task SET crawl_flag = {title_id}, crawl_num = {crawl_num} WHERE id = {task.task_id}"""
    try:
        sqlUtils.exeSql(sql)
    except:
        parse_log.error(f'{task.site_name} title:{title}; SQL error:{str(traceback.format_exc())}')

    return imgListTaskList

# ACG和谐漫画 https://www.acgzone.net/
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
        parse_log.error(f'{task.site_name}  book_title:{book_title}; error:{str(traceback.format_exc())}')
        raise
    path = config.PATH
    head = {}
    # 图片编号
    num = 1
    # 匹配图片列表
    try:
        r = re.search(r'(?<=;var chapterImages = \[).*(?=])', html)
        chapterImages = r.group()
        chapterImages = chapterImages.replace('"', '')
        imgList = re.split(',', chapterImages)
        parse_log.info(f'{task.site_name}  size:{len(imgList)};  imgList:{imgList}')
    except:
        parse_log.error(f'{task.site_name}  error:{str(traceback.format_exc())}')
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
            parse_log.info(f'{task.site_name}  chapter:{imgUrl};  img_filePath:{img_filePath};  img_num:{img_num}')
        except:
            parse_log.warning(f'{task.site_name}  img_filePath:{img_filePath};  warn:{str(traceback.format_exc())}')
        else:
            # 入章节列表队列
            imgName = img_num + '.jpg'
            imgtask = ImgTask(imgUrl=imgUrl, task_id=task.task_id, purl=task.task_url,
                                      filePath=img_filePath, imgName=imgName, head=head, site_name=task.site_name)
            imgTaskList.append(imgtask)
        num += 1

    
    return imgTaskList
    # (?<=;var chapterImages = ).*]
