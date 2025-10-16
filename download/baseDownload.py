import json
import os
import random
import time
import traceback

import config
import requests

from util.logUtil import download_log


class Download:
    
    headers = {}
    params = ""
    
    def __init__(self,headers={},params="") -> None:
        self.headers = headers
        self.params = params
    
    # 页面下载 成功返回html，失败返回false
    def page_down(self, task_url):
        download_log.info(
            f'downloading......   task_url:{task_url}; '
        )
        count = 1
        # 失败则重试
        self.headers.update(config.IMG_LIST_HEAD)
        while count < config.DOWNLOAD_RETRY:
            time.sleep(config.COOL_DOWN * random.random() * count)
            try:
                response = requests.get(task_url,
                                        headers=self.headers,
                                        verify=False,
                                        timeout=config.TIMEOUT)
                # 取页面编码格式进行解码
                try:
                    charset = response.apparent_encoding

                    # 获取编码格式
                    charset = charset.upper()
                    if charset == 'UTF-8':
                        charset = 'UTF-8'
                    elif charset == 'GBK' or charset == 'GB2312':
                        charset = 'GBK'

                    html = response.content.decode(charset)
                except:
                    html = response.content.decode("utf-8")
                response.close()
            except:
                count += 1
                download_log.debug(f'task_url:{task_url};  retry:{count}  error:{traceback.format_exc()}')
            else:
                download_log.info(f'download successful task_url:{task_url}')
                return html
        return False

    # # 组装头
    # def assemblyHeader(self, header, headers):
    #     header.update(headers)
    #     return header

    # upload 上传
    def file_upload(self, filePath, upUrl=config.GOFATS_URL):
        options = {'output': 'json', 'path': '', 'scene': ''}
        count = 1
        while count < config.DOWNLOAD_RETRY:
            count += 1
            with open(filePath, 'rb') as f:
                files = {'file': f}
                res = requests.request('POST', upUrl, data=options, files=files)
                return res
        return False

    # download 下载 成功返回True，失败返回False
    def file_download(self, fileUrl, filePath, timeout=config.TIMEOUT):
        download_log.info(f'downloading......   imgUrl:{fileUrl};  purl:{filePath}')
        count = 1
        # 失败则重试
        while count < config.DOWNLOAD_RETRY:
            time.sleep(config.COOL_DOWN * random.random() * count)
            self.headers.update(config.IMG_HEAD)
            try:
                res = requests.request('GET',
                                        fileUrl,
                                        headers=self.headers,
                                        timeout=timeout,
                                        verify=False)
                # 404 跳出重试
                if res.status_code == 404:
                    download_log.debug(f'fileUrl:{fileUrl}  retry:{count}  code:404')
                    return False
                if res:
                    with open(filePath, 'wb') as f:
                        # 保存
                        f.write(res.content)
                else:
                    raise Exception
            except:
                count += 1
                download_log.debug(f'fileUrl:{fileUrl}  retry:{count}  error:{traceback.format_exc()}')
            else:
                download_log.info(f'download successfull   filePath:{filePath}   fileUrl:{fileUrl}')
                return True
        return False

    # download To upload
    def down_To_up(self, fileUrl, filePath, upUrl=config.GOFATS_URL, timeout=config.TIMEOUT):
        if(self.file_download(fileUrl, filePath, timeout=timeout)):
            resData = self.file_upload(filePath, upUrl=upUrl)
            if resData:
                content = resData.content
                jsonData = json.loads(content)
                url = jsonData['url']
                os.remove(filePath)
                return url
            else:
                download_log.warning(f'upload fail upUrl:{upUrl};  purl:{filePath};')
        else:
            download_log.warning(f'download fail imgUrl:{fileUrl};  purl:{filePath};')