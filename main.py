# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 00:39:59 2023

@author: lin
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')
# %%  导入包
import random
import datetime
from psychopy import monitors, visual, event, core, logging

# %%  gui 获得被试信息
from dt import dt  # 导入自建被试信息函数
data = dt(5)

# %% 设计时间
k = 1
design_time = {'t0': 3 * k,
               't1': '(random.random()+0.5)*k', 't2': '最大为3s', 't3': '3-t1'}
timer = core.Clock()  # 正常计算时间
reverse_timer = core.CountdownTimer()  # 倒计时
# %% 开屏幕 隐藏鼠标   考虑搞成函数 这样玩太麻烦了
if data['id'][0] == 'x00x':  # 如果 没改变id 则开调试小屏
    win = visual.Window(
        size=(640, 360), monitor='testMonitor', screen=-1, color='#010101',
        units='pix')
elif data['id'][0] != 'x00x':  # 改变了id 开正式实验屏

    mon = monitors.Monitor('MyMonitor', width=60.45, distance=60)  # 创建屏幕属性
    mon.setSizePix([1920, 1080])

    win = visual.Window(
        monitor=mon, screen=0, fullscr=True, color='#010101',
        units='pix')  # 正式实验屏大小可能不一致 建议无视警告 单开会卡死 不要单跑这句
    win.mouseVisible = False  # 隐藏鼠标

# %%  材料整理

# %%%  # 指导语
instruction = visual.TextStim(
    win, text=u"Wait for experimenter to start", pos=(0, 0), height=40)
instruction.color = (255, 255, 255)  # 改颜色
# text:文字内容。u'str'，前面加u表示unicode编码,如果是中文的话则需要用u，英文则无需。
#  pos:位置。以屏幕中心(0,0)为坐标中心建一个坐标轴，(x,y)相当于坐标，右/上为正值，左/下为负值

# %%% 注视点
# 注视点  # 改为pix后 height也是像素格式了
fixation = visual.TextStim(win, text='+', height=40)

# %%%  pic 读取在for循环中完成
pic = visual.ImageStim(
    win, size=(320, 180), pos=(-160, 90),
    ori=0, units="pix")  # 图片呈现 参数设置
# pic.pos=(x,x)   # pic.size=(x,x)  修改中心点 和大小
# 可以没有图片位置 后期呈现的时候再添加

pic.image = data['pic'][1]
# %%  画图 多种计时方法
# %%% 方法1 waitKeys

instruction.draw()  # 指导语 3s
win.flip()  # 加; 就可以一行多句运行 类似于r语言  # 指导语
key = event.waitKeys(maxWait=design_time['t0'], keyList=None)  # 等待按键 最多10s

# %%% 方法2 直接 wait

fixation.draw(); win.flip()  # 加; 就可以一行多句运行 类似于r语言  # 注视点
t1 = (random.random() + 0.5) * k  # 1-1.5s 随机出现
core.wait(t1)  # 直接wait 简单直接 不准确 不推荐


# %%% 方法3 while+gettime() 正向计时 只用reset

timer.reset()  # 重置时间点为0s
while timer.getTime() <= 3:
    pic.draw(); win.flip()  # 一行出图 pic

# %%% 方法4 反向计时 记得计时前 reset和设定时间 目前4种方法最准

reverse_timer.reset()
t1 = (random.random() + 0.5) * k
reverse_timer.add(t1)

while reverse_timer.getTime() > 0:
    fixation.draw(); win.flip()

win.close()

# %%% 方法5 帧计时 正规计时 要在所有trail上设置

refresh = 1 / 60
pic_frames = int(3 / refresh)  # 获得帧

event.clearEvents(eventType='keyboard')  # 清空键盘事件
count = -1
timer.reset()  # 重置时间

for frameN in range(pic_frames):
    if 0 <= frameN <= pic_frames:
        pic.draw(); win.flip()

        # 这句不会等待 需要放到while中运行
        key = event.getKeys(keyList=(['space', 'escape']))
        if len(key) != 0:
            data.loc[0, 'rt'] = timer.getTime()  # dataframe赋值
            break
            if key[0] == 'escape':
                win.close()

# %%
# refresh = 1 / 60
# pic_frames = int(3 / refresh)

# for num in range(0, 99):
#     start = datetime.datetime.now()

#     for frameN in range(pic_frames):
#         if 0 <= frameN <= pic_frames:
#             pic.draw(); win.flip()

#     end = datetime.datetime.now()
#     print('程序运行时间为: %s Seconds' % (end - start))
#     print(num)

# %%% 检测吞帧
# pic_frames = int(3 / refresh)

# win.recordFrameIntervals = True
# win.refreshThreshold = 1.0 / 60.0 + 0.004
# logging.console.setLevel(logging.WARNING)

# for num in range(0, 100):
#     start = datetime.datetime.now()

#     pic.image = data['pic'][1]

#     for frameN in range(pic_frames):
#         if 0 <= frameN <= pic_frames:
#             pic.draw(); win.flip()

#     end = datetime.datetime.now()
#     print('程序运行时间为: %s Seconds' % (end - start))
#     print(num)
#     print('Overall, %i frames were dropped.' % win.nDroppedFrames)
