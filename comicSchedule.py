import time
import traceback
from task.chapterListTask import ChapterListTask
import os

from util import sqlUtils
from util.logUtil import except_log, schedule_log
import config
from work.chapterListWork import ChapterListWork
from work.imgListWork import ImgListWork
from work.imgWork import ImgWork
from cache import workQueue, pluginCache

if __name__ == '__main__':
    # 创建目录
    if not os.path.exists(config.PATH):
            os.makedirs(config.PATH)
    
    
    workQueue.init()
    pluginCache.init()

    # 启动线程
    chapterListWorker = ChapterListWork()
    imgListWork = ImgListWork()
    imgWork = ImgWork()

    chapterListWorker.run()
    imgListWork.run()
    imgWork.run()

    selectSql = """
    SELECT id, task_url, task_status, last_crawl_time, next_crawl_time, crawl_cyclicity, crawl_flag, site_name, crawl_num 
    FROM crawl_task 
    WHERE task_status = 0 OR task_status = 1 AND (next_crawl_time <= NOW() OR next_crawl_time is Null)
    """
    while True:
        try:
            # 此处调度应改成单独服务实现
            # 使用 execute()  方法执行 SQL 查询，查询数据库版本
            # fetch_one() 方法查一条数据.
            data = sqlUtils.fetch_one(selectSql)
            if not data:
                schedule_log.debug('task is empty')
                time.sleep(10)
                continue
            schedule_log.info('read task: %s' % (str(data)))
            task_id = data[0]
            # 任务url
            task_url = data[1]
            # 任务状态
            task_status = data[2]
            # 上次抓取时间
            last_crawl_time = data[3]
            # 下次抓取时间
            next_crawl_time = data[4]
            # 抓取周期
            crawl_cyclicity = data[5]
            # 周期抓取标识 唯一id
            crawl_flag = data[6]
            # 抓取站点
            site_name = data[7]
            # 上次抓取章节最大编号
            crawl_num = data[8]
            # 周期任务
            if task_status == 1:
                sql = """
                UPDATE crawl_task 
                SET last_crawl_time = NOW(), next_crawl_time = DATE_ADD(NOW(), INTERVAL + {crawl_cyclicity} MINUTE) 
                WHERE id = {task_id}
                """.format(crawl_cyclicity=crawl_cyclicity,
                            task_id=task_id)
            # 单次任务调出后状态置为 2
            elif task_status == 0:
                sql = """UPDATE crawl_task 
                SET task_status = 2, last_crawl_time = NOW(), next_crawl_time = DATE_ADD(NOW(), INTERVAL + {crawl_cyclicity} MINUTE) 
                WHERE id = {task_id}
                """.format(crawl_cyclicity=crawl_cyclicity,
                            task_id=task_id)
            # 更新调度记录
            try:
                if not sqlUtils.exeSql(sql):
                    raise AssertionError('数据库更新异常')
            except:
                schedule_log.error("SQL:%s   ERROR:%s" %
                                    (sql, str(traceback.format_exc())))
                time.sleep(60)
            else:
                # # 此处应改写前置预处理方法实现（预处理首页请求头等信息，反射任务对应方法，如存在则需要预处理，不存在则证明无需预处理，使用默认头即可）
                # # 反射实现(解析函数命名规则 "imgListParse_" + site_name)
                # functionName = "taskPretreatment_" + task.site_name
                # if hasattr(TaskPretreatment, functionName):
                #     pretreatmentFunction = getattr(TaskPretreatment, functionName)
                #     pretreatmentFunction)
                head = {}

                # 拼任务
                task = ChapterListTask(task_url=task_url,
                                    task_id=task_id,
                                    head=head,
                                    crawl_flag=crawl_flag,
                                    crawl_num=crawl_num,
                                    site_name=site_name)
                # 入队列
                workQueue.put_queue("chapterListQueue",task)
                    
                schedule_log.info('schedule success: %s' % (str(data)))
        except:
            except_log.error('调度异常' + str(traceback.format_exc()))
            time.sleep(360)
