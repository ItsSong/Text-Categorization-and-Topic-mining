#-*- coding: utf-8 -*-
# 功能：对去重后的评价内容进行机械压缩去词处理

import codecs
f = codecs.open('cleanData.txt' ,'r','utf-8')   # 读取评论文件
fileList = f.readlines()
f.close()
f1=codecs.open('ComCleanData.txt','w','utf-8')  # 评论处理后保存路径

for A_string in fileList:
    temp1= A_string.strip('\n')       # 去掉每行最后的换行符'\n'
    temp2 = temp1.lstrip('\ufeff')
    temp3= temp2.strip('\r')
    char_list=list( temp3)           # 将字符串转化列表自动按单个字符分词
    list1=['']
    list2=['']

    # 记录要删除的索引
    del1=[]
    flag=['']
    i=0
    while(i<len(char_list)):
        if (char_list[i]==list1[0]):
            if (list2==['']):
                list2[0]=char_list[i]
            else:
                if (list1==list2):
                    t=len(list1)
                    m=0
                    while(m<t):
                        del1.append( i-m-1)
                        m=m+1
                    list2=['']
                    list2[0]=char_list[i]
                else:
                    list1=['']
                    list2=['']
                    flag=['']
                    list1[0]=char_list[i]
                    flag[0]=i
        else:
            if (list1==list2)and(list1!=[''])and(list2!=['']):
                if len(list1)>=2:
                    t=len(list1)
                    m=0
                    while(m<t):
                        del1.append( i-m-1)
                        m=m+1
                    list1=['']
                    list2=['']
                    list1[0]=char_list[i]
                    flag[0]=i
            else:
                if(list2==['']):
                    if(list1==['']):
                        list1[0]=char_list[i]
                        flag[0]=i
                    else:
                       list1.append(char_list[i])
                       flag.append(i)
                else:
                    list2.append(char_list[i])
        i=i+1
        if(i==len(char_list)):
           if(list1==list2):
                    t=len(list1)
                    m=0
                    while(m<t):
                        del1.append( i-m-1)
                        m=m+1
                    m=0
                    while(m<t):
                        del1.append(flag[m])
                        m=m+1
    a=sorted(del1)
    t=len(a)-1
    while (t>=0):
        #print(char_list[a[t]])
        del char_list[a[t]]
        t=t-1
    str1 = "".join(char_list)
    str2=str1.strip()  # 删除两边空格
    f1.writelines(str2+'\r\n')
f1.close()