# -*- coding:utf-8 -*-
import pandas

"""
Code接口，本地集成Code实现MyCode类。
将数据预处理等方封装在MyCode类中，方便后续调用。
"""


class Code(object):
    """
    Code 类是一个接口，用于定义 Code 类的基本属性和方法，建议继承 Code类的类名设为 MyCode
    """

    def __init__(self, data: pandas.DataFrame):
        """
        初始化函数
        :param data:数据集，将数据集转化为 pandas.DataFrame
        """
        self.data = data

    def get_guide(self):
        """
        该函数为说备注函数，用于返回该数据集合的使用注意事项
        """
        pass

    def get_data(self):
        """
        返回数据样本
        """
        return self.data

    def preprocessing(self):
        """
        数据预处理函数,用于对数据集进行格式、缺失值、异常值等处理
        :return: 处理后的数据集,要求格式为 pandas.DataFrame，
        """
        pass
