#-*- coding: utf-8 -*-

# 第一步：定义特征和目标===========================================================
import pandas as pd
df = pd.read_excel('NewData.xlsx',encoding='utf-8')
X = df[['comment']]
y = df.sentiment


# 第二步：用结巴分词拆分句子为词语=================================================
import jieba
def chinese_cut(mytext):   # 建立一个辅助函数，将分词的结果用空格连接
    return " ".join(jieba.cut(mytext))
X['cut_comment'] = X.comment.apply(chinese_cut) # apply将每一行的评论都进行分词
print("分词之后的前5行是：")
print(X.cut_comment[:5]) # 查看前五行，看分词是否成功


# 第三步：剔除掉停用词、且将词转化为词向量=========================================
# 3.1 定义停用词格式====================
def get_stopwords(file):
    with open(file,encoding='utf-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    new_stopwords_list = [i for i in stopwords_list] # 把停用词作为列表格式保存
    return new_stopwords_list    # 返回存成列表形式的停用词
stopwords = get_stopwords('stoplist.txt')
print("停用词表后10项为：")
print(stopwords[-10:])
# 3.2 向量化============================
max_df = 0.8 # 定义过于平凡的词的界限
min_df = 3   # 定义过于独特的词的界限
from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(max_df = max_df, min_df=min_df, token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b', stop_words=frozenset(stopwords))# 类似于正则表达式
# 使用向量化工具CountVectorizer将评论内容的分词X_train.cut_comment转化为dataframe类型，赋值给transf_matrix
X_train = pd.DataFrame(vect.fit_transform(X.cut_comment).toarray(), columns=vect.get_feature_names())



# 第四步：划分训练集和测试集================================================================
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y, random_state=1)
print("去除停用词且向量化后训练集的格式：")
print(X_train.head())
print("去除停用词且向量化后训练集的大小：",X_train.shape)



# 第五步：选分类器==========================================================================
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split,cross_val_score,StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
models = []
models.append(('LR',LogisticRegression(solver='liblinear',multi_class='ovr')))
models.append(('LDA',LinearDiscriminantAnalysis()))   # 线性判别分析
models.append(('KNN',KNeighborsClassifier()))
models.append(('CART',DecisionTreeClassifier()))
models.append(('NB',MultinomialNB()))
models.append(('SVM',SVC(gamma='auto')))
results = []
names = []
for name,model in models:
    kfold = StratifiedKFold(n_splits=5,random_state=1)  # K交叉验证法
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold,scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s:%f[%f]' %(name,cv_results.mean(),cv_results.std()))
# 画箱线图
plt.boxplot(results,labels=names)
plt.title('algorithm comparision')
plt.show()
# 最终选择分类器为MultinomialNB()


# 第六步：预测==========================================================================
model = MultinomialNB()
model.fit(X_train,y_train)
y_predict = model.predict(X_test)
plt.figure()
plt.plot(range(len(y_test.iloc[:50])),y_test.iloc[:50],'o',markersize=6)
plt.plot(range(len(y_predict[:50])),y_predict[:50],'*',markersize=6)
plt.show()
print("预测Accuracy Rate：",accuracy_score(y_test,y_predict))
print("混淆矩阵：")
print(confusion_matrix(y_test,y_predict))
print("分类报告：")
print(classification_report(y_test,y_predict))



