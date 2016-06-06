# coding=utf-8

"""
@version: 1.0
@author: CordyLiu
@site: 
@software: PyCharm Community Edition
@file: exportText.py
@time: 2016/6/2 11:43

提取指定的文件中的指定字段的文本

"""

import os
import json
import traceback
import toolutil
import conf

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()


class ExportObj(object):
    """
    提取对象
    """
    def __init__(self):

        ''' 已经翻译过的dic '''
        self.languageDic = {}

        ''' 后续的编号 '''
        self.textNum = conf.NUMBER_BEGIN

        self.isNeedLoadLanguage = False


    def getTextKey(self):
        """
        format 一个特定的标记key 出来
        :return:
        """
        textKey = conf.ID_FORMAT % self.textNum
        self.textNum += 1
        return textKey


    def init(self):
        """
        是否存在文件夹
        :return:
        """
        ''' 如果没有文件夹, 创建一个文件夹, 与临时文件 '''
        if os.path.exists(conf.LANGUAGE) is not True:
            os.makedirs(conf.LANGUAGE)

        ''' 提取完成后的文本存放, 初始化 '''
        languageFile = open(os.path.join(conf.LANGUAGE, conf.RESOURCE_LANGUAGE_FILENAME), 'w')
        languageFile.close()

        fileUrl = os.path.join(conf.LANGUAGE, conf.LANGUAGE_TMP)
        if os.path.exists(fileUrl) is not True:
            ''' 创建一个 '''
            file = open(fileUrl, 'w')
            file.close()
        else:
            ''' 表示已经存在了, 需要把文本中的内容转换成dic， key：简体中文 value: 转换的语言 '''
            self.isNeedLoadLanguage = True


    def do(self, readPath):
        """
        进行翻译文本的提取
        :return:
        """
        ''' 初始化相关东西 '''
        self.init()

        ''' 读取已经翻译过的文本 '''
        self.doReadLanguage()

        ''' 提取文本 '''
        writePath = os.path.join(conf.LANGUAGE, conf.RESOURCE_TMP_DATA_PATH)
        self.doExport(readPath, writePath)

        ''' copy一份用于翻译的原始文件出来，用于后面保存 '''
        self.doCopyFile()


    def doReadLanguage(self):
        """
        读取已经翻译过的文本
        :return:
        """
        if self.isNeedLoadLanguage == False:
            return

        ''' 提取完成后的文本存放的 '''
        fileUrl = os.path.join(conf.LANGUAGE, conf.LANGUAGE_TMP)
        self.languageDic = toolutil.loadJsonFile(fileUrl)


    def doExport(self, readPath, writePath):
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
                self.exportFile(rfileJsonPath, wfileJsonPath)

        print u"提取完成................."


    def doCopyFile(self):
        """
        copy language.txt 文件
        :return:
        """
        try:
            sourceFile = open(os.path.join(conf.LANGUAGE, conf.RESOURCE_LANGUAGE_FILENAME), "rb")
            targetFile = open(os.path.join(conf.LANGUAGE, conf.RESOURCE_LANGUAGE_BAK_FILENAME), "wb")
            targetFile.write(sourceFile.read())

        except:
            print traceback.print_exc()
        finally:
            targetFile.close()
            sourceFile.close()


    def exportFile(self, rFile, wFile):
        """
        文件转换
        :param rFile: 被转换的文件
        :param wFile: 转换后的文件
        :return:
        """
        try:
            rf = open(rFile, 'r')
            wf = open(wFile, 'w')

            ''' 提取完成后的文本存放的 '''
            languageFile = open(os.path.join(conf.LANGUAGE, conf.RESOURCE_LANGUAGE_FILENAME), 'a')

            ''' 一行一行的读, 并写入到文件中去 '''
            for line in rf:
                languageText = ''
                for convertKey in conf.CONVERT_KEY_ARRAY:
                    if line.find(convertKey) <= 0:
                        continue

                    ''' 表示有这个key, 需要提取出对应的东西 '''
                    targetValue = self.getLineJsonValue(line)
                    if targetValue == None:
                        continue

                    ''' 处理换行符 '''
                    targetValue = targetValue.replace('\n', '\\n')
                    print targetValue.find('\n')
                    print "targetValue.....", targetValue, type(targetValue)

                    ''' 如果已经翻译完成了，直接替换掉 '''
                    languageValue = self.languageDic.get(targetValue.decode('utf-8'))

                    if languageValue != None:
                        ''' 表示有这个值 '''
                        line = line.replace(targetValue, languageValue.encode('utf-8'))
                    else:
                        textKey = self.getTextKey()
                        languageText = textKey + targetValue + '\n'
                        ''' 替换掉对应数据 '''
                        line = line.replace(targetValue, textKey)

                    if isinstance(line, unicode):
                        line = line.encode('utf-8')

                ''' 需要进行写的操作'''
                wf.write(line)

                ''' 写入提取的文本 '''
                if languageText != None and len(languageText) > 0:
                    languageFile.write(languageText)

        except:
            print traceback.print_exc()
        finally:
            rf.close()
            wf.close()
            languageFile.close()


    def getLineJsonValue(self, text):
        """
        得到json格式的文本一行的对应的key 的值的数据, 一定要按下面的格式写 "key" : "value",
        '''  "text" : "<l c=FF6633>二连击<\/l>伤害还不够，让我们进一步打出<l c=FF6633>三连击<\/l>，让刘备来帮忙吧！", '''
        :param text:
        :return:
        """
        ''' 按 " 号分开后得到一个数组, 只有文本才能替换 '''
        stringArray = text.split('"')
        if len(stringArray) != 5:
            ''' 表示不符合符合标准 '''
            return None

        return stringArray[3]


if __name__ == '__main__':
    obj = ExportObj()
    line = '我……（刚那个梦还是先别说出来吧。）\\n没问题！那有时空秘钥的线索吗？'
    line1 = line.replace('\\n', '\n')
    print line1.replace('\n', '\\n')

    # obj.do(conf.RESOURCE_READ_DATA_PATH)