# coding=utf-8

"""
@version: 1.0
@author: CordyLiu
@site: 
@software: PyCharm Community Edition
@file: conf.py
@time: 2016/6/4 15:03

配置文件，相关的东西都在这个文件的中配置
带 ***** 不需要改变参数

"""

''' 特定语言的翻译后的文件夹 '''
LANGUAGE = 'EN'

''' 最原始的资源路径 '''
RESOURCE_READ_DATA_PATH = ''

''' 最后写入的资源路径 '''
RESOURCE_WRITE_DATA_PATH = 'DATA'

''' json中需要转换的key '''
CONVERT_KEY_ARRAY = ['"name"', '"text"', '"textForActor"', '"actorName"', '"title"']

''' 中间暂存的资源路径 ***** '''
RESOURCE_TMP_DATA_PATH = 'tmp'

''' 转换的翻译文件, 导出与导入都用这个 ***** '''
RESOURCE_LANGUAGE_FILENAME = 'language.txt'

''' 转换的翻译文件, 备份的翻译文件 ***** '''
RESOURCE_LANGUAGE_BAK_FILENAME = 'language_bak.txt'

''' 编号开始值 ***** '''
NUMBER_BEGIN = 100001

''' 特定格式的编号， 和下面的正则表示式是有关联的 ***** '''
ID_FORMAT = '#%s#:'

''' 从头开始匹配 '#10001#:' 的串, 正则表达式 ***** '''
ID_FORMAT_RULE = r'#\d+#:'

''' 记录已经翻译过的文件，这个文件不要去动 ***** '''
LANGUAGE_TMP = 'tmp.txt'
