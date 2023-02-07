# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 00:40:36 2023

@author: lin
"""

from psychopy import gui, data


def info():
    """
    gui界面收集被试信息,被试不填,有默认填写

    Arguments 无

    Returns:
        exp_info (dict): 内有所有收集的被试信息
        控制台中 根据gui按键情况返回被试信息和取消信息

    Note: gui界面可自由根据需求改变,不唯一
    """

    exp_info = {
        "id": "x00x",
        "exp_time": data.getDateStr(),
        "gender": ["男", "女"],
        "age": 0,
    }

    infoDlg = gui.DlgFromDict(
        dictionary=exp_info,
        title="基本信息",
        fixed=["exp_time"],
        screen=-1,
        order=["id", "exp_time", "gender", "age"],
    )

    if infoDlg.OK:  # 点击OK
        print(exp_info)  # 可丰富
    else:  # 点击取消
        print("cancel")

    return exp_info
