# COMIC-CRAWL

## 2.0
### fix
* 修改代码整体结构。将解析部分改为模块形式，统一放在 plugin 下   
* 将旧的解析部分拆分成模块

### add
* 增加动态加载解析模块功能。添加新的解析模块无需重启服务，当读取到新站点任务时，会自动加载对应站点名的模块
* 新增解析模块 iimanhua 
***


## 1.10
### fix
* 优化解析流程，改进解析模块众多解析不方便维护问题
***


## 1.9
### add
* 新增 mkzhan 
* 新增 alimanhua
***

## 1.6
### fix 
* 优化下载流程
### add
* 新增 zuimh
* 新增 alimanhua
***

## 1.3    
### add
* 新增周期增量采集功能
* 新增指定采集范围功能
***

## 1.1
### add
* 新增 acgzone
* 新增 36mh
***

## 1.0
* 漫画采集框架，通过漫画列表首页 URL 采集整本漫画
