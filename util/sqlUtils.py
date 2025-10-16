import pymysql
import psycopg2
from util.logUtil import except_log
from dbutils.pooled_db import PooledDB
import traceback
import time
import config

###################### SQL #########################
DB_POOL = {
    'creator': psycopg2,
    # 'charset': config_template['MYSQL']['CHARSET'],
    'maxconnections': 3,  # 连接池最大连接数量
    # 'cursorclass': pymysql.cursors.DictCursor
}

DB_POOL.update(config.DB_INFO)

# DB_POOL = {
#     'creator': pymysql,
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'password': 'root',
#     'db': 'crawl',
#     # 'charset': config_template['MYSQL']['CHARSET'],
#     'maxconnections': 3,  # 连接池最大连接数量
#     # 'cursorclass': pymysql.cursors.DictCursor
# }

POOL = PooledDB(**DB_POOL)


# 连接
def create_conn():
    try:
        conn = POOL.connection()
        cursor = conn.cursor()
        return (conn, cursor)
    except:
        except_log.error("ERROR:%s" % (str(traceback.format_exc())))
        time.sleep(60)


# 关闭
def close_conn(conn, cursor):
    cursor.close()
    conn.close()


# 执行sql
def exeSql(sql):
    """
    UPDATE table SET key=value, ...
    INSERT INTO table (key, ...) VALUES (value, ...)
    DELETE FROM table WHERE ...
    """
    res = False
    try:
        conn, cursor = create_conn()
        cursor.execute(sql)
        # res = cursor.execute(sql)
        conn.commit()
    except:
        except_log.error("SQL:%s   ERROR:%s" %
                         (sql, str(traceback.format_exc())))
        # 失败回滚
        conn.rollback()
    else:
        res = True
    finally:
        close_conn(conn, cursor)
    return res


# 查一条
def fetch_one(sql):
    res = False
    try:
        conn, cursor = create_conn()
        cursor.execute(sql)
        res = cursor.fetchone()
    finally:
        close_conn(conn, cursor)
    return res


# 查全部
def fetch_all(sql):
    res = False
    try:
        conn, cursor = create_conn()
        cursor.execute(sql)
        res = cursor.fetchall()
    finally:
        close_conn(conn, cursor)
    return res

# 删除

# 执行sql语句
