# coding=utf-8

"""
@version: 1.0
@author: CordyLiu
@site:
@software: PyCharm Community Edition
@file: toolutil.py
@time: 2016/6/2 11:43

一些文件的获取方法

"""


import traceback
import os
import codecs
import json

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()


def getAllFileAndDirByPath(path):
    """
    获取某个路径下的所有文件和文件夹.不会递归去查询文件夹下的文件
    :param path: 指定文件夹路径
    :return:
    """
    dirArray = []
    fileArray = []
    try:
        fileNameArray = os.listdir(path)
        for fileName in fileNameArray:
            fullPath = os.path.join(path, fileName)

            #print "fullPath --> ", fullPath
            #文件夹
            if os.path.isdir(fullPath) == True:
                dirArray.append(fileName)

            #文件
            elif os.path.isfile(fullPath) == True:
                fileArray.append(fileName)
    except:
        print traceback.print_exc()
    finally:
        return fileArray, dirArray


def getFileBySuffix(path, suffix):
    """
    获取这个目录以某个后缀结尾的文件.ect: .txt
    :param path: 指定的目录
    :param suffix: 指定的后缀
    :return:
    """
    resultFileArray = []
    fileArray, dirArray = getAllFileAndDirByPath(path)
    for fileName in fileArray:
        try:
            fileNameSuffix = os.path.splitext(fileName)[1]
            if fileNameSuffix == suffix:
                resultFileArray.append(fileName)
        except:
            print traceback.print_exc()

    return resultFileArray


def trimBom(tmpStr):
    """
    去掉编码的bom的数据
    :return:
    """
    if not tmpStr:
       return ''

    if len(tmpStr) < 3:
        return ''

    if tmpStr[:3] == codecs.BOM_UTF8:
        return tmpStr[3:]

    return tmpStr


def getResourceDataPath(path):
    """
    获取资源数据的path
    :return:
    """
    return os.path.abspath(os.path.join(os.getcwd(), path))


def getAllDirArray(fullPath):
    """
    得到所有的剧情文件夹
    :param fullPath: 全路径
    :return:
    """
    fileArray, dirArray = getAllFileAndDirByPath(fullPath)
    return fileArray, dirArray


def getJsonFileArrayByPath(path):
    """
    解析一个文件夹下面的所有的文件json文件
    必须以.json结尾的文件
    :return:
    """
    return getFileBySuffix(path, '.json')


def loadJsonFile(path):
    """
    加载json文件
    :return:
    """
    try:
        f = open(path, 'rb')
    except:
        print traceback.format_exc()
        print "path error", path

    ''' json 转换 '''
    try:
        jsonData = f.read()
        if jsonData == None or len(jsonData) <= 0:
            return {}

        jsonData = trimBom(jsonData)
        return Decoder.decode(jsonData)
    except:
        print traceback.format_exc()
        print "path error 2", path
    finally:
        f.close()



if __name__ == '__main__':
    pass




