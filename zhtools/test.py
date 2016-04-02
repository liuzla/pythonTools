# coding:utf-8
"""
Created on 2016/4/1

单元测试

@author: Cordial
"""
from unittest import TestCase

from langconv import *

class ConverterTest(TestCase):
    def assertConvert(self, name, string, converted):
        c = Converter(name)
        new = c.convert(string)
        assert new == converted, (
                "convert(%s, '%s') should return '%s' but '%s'" % (
                    repr(name), string, converted, new)).encode('utf8')

    def assertST(self, trad, simp):
        if not py3k:
            trad = trad.decode('utf-8')
            simp = simp.decode('utf-8')
        self.assertConvert('zh-hans', trad, simp)
        self.assertConvert('zh-hant', simp, trad)

    def test_zh1(self):
        self.assertST('乾燥', '干燥')
        self.assertST('乾坤', '乾坤')
        self.assertST('乾隆', '乾隆')
        self.assertST('幹事', '干事')
        self.assertST('牛肉乾', '牛肉干')
        self.assertST('相干', '相干')


if '__main__' == __name__:
    import unittest
    unittest.main()


