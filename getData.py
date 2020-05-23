#-*- coding: utf-8 -*-
# 功能：从表中提取评论内容并保存为txt文件

import pandas as pd
# 获取评论数据
data = pd.read_csv('data.csv', encoding = 'gbk')
data = data[[u'comment']]
# 保存
data.to_csv('comment.txt', index = False, header = False, encoding = 'utf-8')

