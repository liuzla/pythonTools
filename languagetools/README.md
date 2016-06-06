# languagetools

**********************************************
所有的配置文件都是在conf.py下面
操作：1，确认转换的语言版本，所有的临时文件都在 LANGUAGE 指定的文件夹下面
     2，确认原始的简体版资源的路径 （RESOURCE_READ_DATA_PATH）
     3，确认最后转换后的资源路径 （RESOURCE_WRITE_DATA_PATH）
     4，执行导出操作（export）
     5，找到 LANGUAGE 文件下需要翻译文件（language.txt），翻译后替换掉这个文件（其他的文件不要去动）
     6，执行导入操作（import）
     7，完成后 RESOURCE_WRITE_DATA_PATH 路径下有就是转换后的文件
**********************************************
