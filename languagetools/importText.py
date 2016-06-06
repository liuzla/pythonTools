# coding=utf-8

"""
@version: 1.0
@author: CordyLiu
@site: 
@software: PyCharm Community Edition
@file: exportText.py
@time: 2016/6/3 12:21

把翻译过后的文本导入到文件中

"""

import os
import json
import traceback
import toolutil
import conf
import re

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()


class ImportObj(object):
    """
    导入的对象
    """
    def __init__(self):

        ''' 翻译过的文本 {key：翻译文} '''
        self.importTextDic = {}

        ''' 翻译前的文本 {key：简体} '''
        self.cnTextDic = {}

        ''' 已经翻译过的文件 {简体：翻译文} '''
        self.languageDic = {}

        ''' 正则表达式的模板对象 '''
        self.pattern = re.compile(conf.ID_FORMAT_RULE)


    def do(self, writePath):
        """
        做对应的操作
        :return:
        """
        ''' 先导入翻译文件转成dic '''
        self.doLanguageToDic()

        ''' 在导入被翻译的文件 '''
        self.doCnToDic()

        ''' 已经翻译过的文件 {简体：翻译文}导入 '''
        self.doReadLanguage()

        ''' 翻译文件 '''
        readPath = os.path.join(conf.LANGUAGE, conf.RESOURCE_TMP_DATA_PATH)
        self.doImport(readPath, writePath)

        ''' 记录已经翻译的文本 '''
        self.doWriteLanguage()


    def doReadLanguage(self):
        """
        读取已经翻译过的文本
        :return:
        """
        ''' 提取完成后的文本存放的 '''
        fileUrl = os.path.join(conf.LANGUAGE, conf.LANGUAGE_TMP)
        self.languageDic = toolutil.loadJsonFile(fileUrl)


    def doWriteLanguage(self):
        """
        把 self.languageDic 记录到文本中去
        :return:
        """
        try:
            file = open(os.path.join(conf.LANGUAGE, conf.LANGUAGE_TMP), 'wb')
            file.write(Encoder.encode(self.languageDic))
        except:
            print traceback.print_exc()
        finally:
            file.close()


    def doLanguageToDic(self):
        """
        导入文本的中的翻译文件，转换成功dic
        :return:
        """
        try:
            ''' 提取完成后的文本存放的 '''
            languageFile = open(os.path.join(conf.LANGUAGE, conf.RESOURCE_LANGUAGE_FILENAME), 'r')

            ''' 一行一行的读, 读取进来, 构建一个匹配的模板 '''

            for line in languageFile:
                if line == None or len(line) <= 0:
                    continue

                ''' 去掉换行符 '''
                line = line.strip('\n')
                matchObj = self.pattern.match(line)
                if matchObj == None:
                    print "转换字符串的格式错误（'#10001#:' 开头）........", line
                    raise

                ''' 把字符串转换成dic, 然后那匹配到的字符串做key， value(后面的字符串) '''
                bIndex, eIndex = matchObj.span()
                self.importTextDic[line[bIndex:eIndex]] = line[eIndex::]

            print u"加载翻译文本成功...................."

        except:
            print traceback.print_exc()
        finally:
            languageFile.close()


    def doCnToDic(self):
        """
        导入文本的中的简体的文件，转换成功dic
        :return:
        """
        try:
            ''' 提取完成后的文本存放的 '''
            languageFile = open(os.path.join(conf.LANGUAGE, conf.RESOURCE_LANGUAGE_BAK_FILENAME), 'r')

            ''' 一行一行的读, 读取进来, 构建一个匹配的模板 '''

            for line in languageFile:
                if line == None or len(line) <= 0:
                    continue

                ''' 去掉换行符 '''
                line = line.strip('\n')
                matchObj = self.pattern.match(line)
                if matchObj == None:
                    print "转换字符串的格式错误（'#10001#:' 开头）........", line
                    raise

                ''' 把字符串转换成dic, 然后那匹配到的字符串做key， value(后面的字符串) '''
                bIndex, eIndex = matchObj.span()
                self.cnTextDic[line[bIndex:eIndex]] = line[eIndex::]

            print u"加载简体文本成功...................."

        except:
            print traceback.print_exc()
        finally:
            languageFile.close()


    def doImport(self, readPath, writePath):
        """
        提取指定的文件夹下面所有文件
        :return:
        """
        ''' 得到读取的指定的文件的数据 '''
        readFullPath = toolutil.getResourceDataPath(readPath)
        writeFullPath = toolutil.getResourceDataPath(writePath)

        ''' 得到所有的文件夹, 不需要管里面的文件 '''
        readFileArray, readDirNameArray = toolutil.getAllDirArray(readFullPath)

        if readDirNameArray == None or len(readDirNameArray) <= 0:
            print "指定的文件下面没有文件..............."
            return

        ''' 遍历所有的文件夹 '''
        for DirName in readDirNameArray:
            ''' 文件名都是, 只转换json 格式的文件 '''
            readFullFilePath = os.path.join(readFullPath, DirName)
            writeFullFilePath = os.path.join(writeFullPath, DirName)
            readJsonFileArray = toolutil.getJsonFileArrayByPath(readFullFilePath)
            if readJsonFileArray == None or len(readJsonFileArray) <= 0:
                continue

            ''' 如果没有文件夹, 创建一个文件夹 '''
            if os.path.exists(writeFullFilePath) is not True:
                os.makedirs(writeFullFilePath)

            ''' 解析json '''
            for fileJsonName in readJsonFileArray:
                rfileJsonPath = os.path.join(readFullFilePath, fileJsonName)
                wfileJsonPath = os.path.join(writeFullFilePath, fileJsonName)
                self.importFile(rfileJsonPath, wfileJsonPath)

        print u"翻译成功................."


    def importFile(self, rFile, wFile):
        """
        文件转换，翻译成功指定的语言
        :param rFile: 被转换的文件
        :param wFile: 转换后的文件
        :return:
        """
        try:
            rf = open(rFile, 'r')
            wf = open(wFile, 'w')

            ''' 一行一行的读, 并写入到文件中去 '''
            for line in rf:
                matchObj = self.pattern.search(line)
                if matchObj != None:
                    ''' 表示匹配到对应的文本，然后需要从dic中找对应的值 '''
                    replStr = self.importTextDic.get(matchObj.group())
                    if replStr == None:
                        print "对应的文件：",  rFile
                        print "内容：", line
                        print "找不到对应的翻译后的文件", matchObj.group()
                        raise

                    line = self.pattern.sub(replStr, line)

                    ''' 保存到已经翻译的文本中去 '''
                    cnText = self.cnTextDic.get(matchObj.group())
                    if cnText != None:
                        self.languageDic[cnText] = replStr

                if isinstance(line, unicode):
                    line = line.encode('utf-8')

                ''' 需要进行写的操作'''
                wf.write(line)

        except:
            print traceback.print_exc()
        finally:
            rf.close()
            wf.close()


if __name__ == '__main__':
    # convertFile(u'4回合2刘备进场.json', '22.json')
    ''' 当前语言版本 '''
    obj = ImportObj()
    obj.do(conf.RESOURCE_WRITE_DATA_PATH)
