#-*- coding: utf-8 -*-
# 功能：打标签（正面情感：1；负面情感：0）

import pandas as pd
df = pd.read_csv('data.csv',encoding='gbk')

# 定义函数：将评论内容分为两类，正面为1；负面为0
def make_label(df):
    df["sentiment"] = df["star"].apply(lambda x: 1 if x>3 else 0)
    # 评星数量>3的：正向情感，取值为1；反之视作负向情感，取值为0
    df.to_excel('NewData.xlsx',encoding='utf-8')

# 调用函数
make_label(df)
print(df.head())