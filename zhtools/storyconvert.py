# coding:utf-8
"""
Created on 2016/4/1

策划的剧情转换

@author: Cordial
"""

import os
import json
import traceback
import toolutil

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()


''' 转换的资源路径 '''
RESOURCE_READ_DATA_PATH = ''
RESOURCE_WRITE_DATA_PATH = ''

''' json中需要转换的key '''
CONVERT_KEY_ARRAY = ['"name"', '"text"']



def storyConvertFT(readPath, writePath, convertType):
    """
    剧情的转换繁体
    :return:
    """
    ''' 得到读取的指定的文件的数据 '''
    readFullPath = toolutil.getResourceDataPath(readPath)
    writeFullPath = toolutil.getResourceDataPath(writePath)

    ''' 得到所有的文件夹, 不需要管里面的文件 '''
    readFileArray, readDirNameArray = toolutil.getAllDirArray(readFullPath)

    if readDirNameArray == None or len(readDirNameArray) <= 0:
        print "读取的指定的文件下面没有文件..............."
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
            convertFile(rfileJsonPath, wfileJsonPath, convertType)

    print "转换完成................."


def convertFile(rFile, wFile, convertType='zh-hant'):
    """
    文件转换
    :param rFile: 被转换的文件
    :param wFile: 转换后的文件
    :param convertName: 转换类型, 默认为转成繁体
    :return:
    """
    try:
        rf = open(rFile, 'r')
        wf = open(wFile, 'w')

        ''' 一行一行的读, 并写入到文件中去 '''
        for line in rf:
            for convertKey in CONVERT_KEY_ARRAY:
                if line.find(convertKey) <= 0:
                    continue

                ''' 表示有这个key, 需要转换, 转成功需要变成str 类型进行写 '''
                line = toolutil.convertString(line)
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
    # LANGUAGE = 'CN' 简体
    # LANGUAGE = 'TW' 繁体
    # LANGUAGE = 'EN' 英文
    # LANGUAGE = 'JP' 日文

    # 'zh-hans' 简体
    # 'zh-hant' 繁体

    RESOURCE_READ_DATA_PATH = 'D:\BlackSG\BlackSGServer\data\story'
    RESOURCE_WRITE_DATA_PATH = 'D:\BlackSG\BlackSGServer\data\story\TH'
    storyConvertFT(RESOURCE_READ_DATA_PATH, RESOURCE_WRITE_DATA_PATH, 'zh-hans')



