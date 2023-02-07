# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 13:08:38 2023

@author: lin
"""

import pandas as pd
import numpy as np

from info import info  # 导入自建被试信息函数


def dt(trail):
    """
    根据需求获得初始的 DataFrame  ,已经将gui获得被试信息内置,改动gui找 info()函数

    Arguments
        trail(num):实验次数,用于保证长度

    Returns:
        dt (DataFrame): 内有实验所有信息(被试信息 反应时 按键等)

    Note: 根据需求自改
        未考虑block 随机等问题 !!!

    """
    basic_info = info()  # gui获得被试信息

    dt_dict = {}
    for num in range(0, len(basic_info)):  # 建议理解 [list(basic_info.values())[0]]
        dt_dict[list(basic_info.keys())[num]] = [
            list(basic_info.values())[num]] * trail  # 将基本信息中得到的值扩列

    def add_postfix(x):
        x = str(x)
        return x + '.jpg'  # 根据图片改这块 目的是批量出 'x.jpg'这样的文字

    dt_dict['pic'] = list(map(add_postfix, np.random.randint(1, 3, trail)))

    dt_dict['rt'] = np.zeros(trail)  # 给字典加参数 记得长度要一致 根据需求自己加

    data = pd.DataFrame(dt_dict)  # 字典转 dataframe

    print(dt_dict.keys())

    return data


"""2. 方法:总体目标一个目标应该是减少rt的可变性和漂移。
第二个目标应该是消除疲劳、练习、动机和任何其他未明确控制的因素在不同条件下的系统性差异。
第三个目标应该是让受试者表现得“最佳”。(但“最佳”在这里并没有很好地定义。)
个体差异的普遍存在，证明了在任何可能的情况下都应该进行主体内部的比较。
普遍存在的减速实践效应表明，需要检查趋势
,在收集主要利益数据之前尝试实现某种程度的稳定性，并平衡这些影响。
为了尽量减少变化，需要尽量减少警觉性/疲劳和动机的变化。"""
