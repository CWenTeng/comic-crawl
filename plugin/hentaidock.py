from util.logUtil import parse_log
from util import utils
import traceback
import config
from lxml import etree
import re
import os
from task.imgTask import ImgTask
from download.baseDownload import Download


def chapter_list_parse(html, task):
    return img_list_parse(html, task)

# hentaidock 漫画
def img_list_parse(html, task):
    html = etree.HTML(html)
    path = config.PATH + '/Erocool'
    imgTaskList = []
    try:
        # 标题
        # title = html.xpath("//meta[@name='description']/@content")[0]
        book_title = html.xpath("//title/text()")[0]
        book_title = re.sub(' +', ' ', book_title)
        # 格式化
        book_title = utils.formatting(book_title)
        parse_log.info(f'hentaidock   book_title: {book_title}')
        try:
            # 创建漫画书目录
            book_filePath = '/'.join([path, book_title])
            if not os.path.exists(book_filePath):
                os.makedirs(book_filePath)
        except:
            parse_log.error(f'hentaidock   book_title:{book_title}; error:{traceback.format_exc()}')
            raise

        # 图片列表
        imgUrls = html.xpath("//div[@class='flex flex-wrap content-center justify-center']")
        imgUrls = imgUrls[0].xpath(".//img/@data-src")
        parse_log.info(f"hentaidock  imgSize:{len(imgUrls)};  imgUrls:{imgUrls}")
        # 封面
        # HomeImg = ''
        imgNum = 1
        # 遍历列表
        for imgUrl in imgUrls:
            try:
                imgName = str(imgNum) + '.jpg'
                # 拼装任务
                imgtask = ImgTask(imgUrl=imgUrl, task_id=task.task_id, filePath=book_filePath, imgName=imgName,
                                          head=task.head, purl=task.task_url, site_name=task.site_name)
                imgTaskList.append(imgtask)
                # 入图片队列
                # workQueue.put_queue("imgQueue",imgtask)
                # 协程
                # gevent.spawn(img.imgDown,imgUrl,filePath,imgName).join()
            except:
                parse_log.warning(f'hentaidock   imgUrl:{imgUrl};  imgName:{imgName};  filePath:{book_filePath};   warn: {traceback.format_exc()}')
            imgNum += 1
        # 下载封面
        if imgUrls[0]:
            try:
                # imgtask = imgTask.imgTask(imgUrl=imgUrls[0], task_id=task.task_id, filePath=book_filePath,
                #                           imgName='HomeImg.jpg', purl=task.task_url, site_name=task.site_name)
                filePath = '/'.join([book_filePath, "HomeImg.jpg"])
                Download().file_download(fileUrl=imgUrls[0], filePath=filePath)
            except:
                parse_log.warning(f'hentaidock   HomeImg warn:{traceback.format_exc()}')
    except:
        parse_log.error(f'hentaidock  error:{traceback.format_exc()}')

    return imgTaskList
