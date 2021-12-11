#################### settings #####################
DOWNLOAD_RETRY = 3  # 下载重试次数
RETRY = 7  # 放回队列重试次数 -1无限重试
TIMEOUT = 50  # 最大超时
COOL_DOWN = 10  # 冷却
PATH = '/home/pi/share/share1/comic'  # 下载路径
# PATH = 'G:/123'    #下载路径
# PATH = 'D:/'    #下载路径
##################### gofast #######################
GOFATS_URL = 'http://localhost:8080/group1/upload'
#################### 图片下载线程数 #################
IMG_DOWNLOAD_THREAD = 3
# 图片列表
IMG_LIST_THREAD = 2
# 章节列表
CHAPTER_LIST_THREAD = 1
###################### UA #########################
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
SEC_CH_UA = '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"'
#################### HEADER #######################
# 图片列表
IMG_LIST_HEAD = {
    'user-agent': UA,
    # 'sec-ch-ua':SEC_CH_UA,
    'sec-ch-ua-mobile': '?0',
    'ec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'cache-control': 'max-age=0'
    # 'sec-fetch-site':'same-origin',
    # 'accept-encoding':'gzip, deflate, br',
    # 'accept-language':'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7'
}
# 图片
IMG_HEAD = {
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': UA,
    # 'sec-ch-ua':SEC_CH_UA,
    'sec-ch-ua-mobile': '?0',
}

###################### SQL #########################
DB_INFO = {
    'host': '192.168.1.107',
    'port': 3306,
    'user': 'crawl',
    'password': 'crawlpi',
    'db': 'crawl',
    # 'charset': config_template['MYSQL']['CHARSET'],
    'maxconnections': 3,  # 连接池最大连接数量
    # 'cursorclass': pymysql.cursors.DictCursor
}
