# -*- codeing = utf-8 -*-
# @Time 2022/3/25 20:30
# @Author : 黄康
# @file : main.py
# @Software : PyCharm

# 导入networkx，matplotlib包
import re

import networkx as nx
import matplotlib.pyplot as plt
import jieba.posseg as pseg  # 引入词性标注接口
# 导入random包
import random
import codecs
# 导入pyecharts
from pyecharts import options as opts
# pyecharts 柱状图
from pyecharts.charts import Bar
# pyecharts 词云图
from pyecharts.charts import WordCloud
# 词云
import wordcloud
import imageio

# 定义主要人物的个数
keshihuaTop=10  # 可视化人物图人数
mainTop = 100  # 人物词云图人物数
peopleTop=10  # 人物关系图

# 获取小说文本
# 读取文件
fn = open('prepare/天龙八部.txt', encoding="utf-8")
string_data = fn.read()  # 读出整个文件
fn.close()  # 关闭文件

# 文本预处理
pattern = re.compile(u'\t|\s|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
txt = re.sub(pattern, '', string_data)  # 将符合模式的字符去除
print('预处理完毕')



# 停词文档
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


stopwords = stopwordslist('prepare/tingyong.txt')


# 通过键值对的形式存储词语及其出现的次数
counts1 = {}   # 存放词性词频
counts2={}  #存放人物词频
# # 生成词频词性文件
def getWordTimes1():
    cutFinal = pseg.cut(txt)

    for w in cutFinal:
        if w.word in stopwords or w.word == None:
            continue
        else:
            real_word = w.word+'_'+w.flag
        counts1[real_word] = counts1.get(real_word, 0) + 1

getWordTimes1()

items1 = list(counts1.items())
# 进行降序排列 根据词语出现的次数进行从大到小排序
items1.sort(key=lambda x: x[1], reverse=True)


# 导出数据
# 分词生成人物词频（写入文档）
def wordFreq1(filepath, topn1):
    with codecs.open(filepath, "w", "utf-8") as f:
        for i in range(topn1):
            word, count = items1[i]
            f.write("{}:{}\n".format(word, count))


# 生成词频文件
wordFreq1("output/天龙八部词频词性.txt", 300)

# 将txt文本里的数据转换为字典形式
fr1 = open('output/天龙八部词频词性.txt', 'r', encoding='utf-8')
dic1 = {}
keys1 = []  # 用来存储读取的顺序
for line in fr1:
    # 去空白,并用split()方法返回列表

    v1 = line.strip().split(':')


    dic1[v1[0]] = v1[1]
    keys1.append(v1[0])
fr1.close()

list_name1 = list(dic1.keys())  # 人名
list_name_times1 = list(dic1.values())  # 提取字典里的数据作为绘图数据
def  create_wordproperties():
    bar1 = Bar()
    bar1.add_xaxis(list_name1[0:keshihuaTop])
    bar1.add_yaxis("词语出现次数", list_name_times1,color='blue')
    bar1.set_global_opts(title_opts=opts.TitleOpts(title="词频词性可视化图", subtitle="词频词性top10"),
                        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}))
    bar1.set_series_opts(label_opts=opts.LabelOpts(position="top"))

    # 生成 html 文件
    bar1.render("output/天龙八部词频词性可视化图.html")

# 得到 分词和出现次数
def getWordTimes2():
    # 分词，返回词性
    poss = pseg.cut(txt)
    for w in poss:
        if w.flag != 'nr' or len(w.word) < 2:
            continue  # 当分词长度小于2或该词词性不为nr（人名）时认为该词不为人名

        else:
            real_word = w.word
        counts2[real_word] = counts2.get(real_word, 0) + 1


getWordTimes2()
items2 = list(counts2.items())
# 进行降序排列 根据词语出现的次数进行从大到小排序
items2.sort(key=lambda x: x[1], reverse=True)


# 导出数据
# 分词生成人物词频（写入文档）
def wordFreq2(filepath, topn):
    with codecs.open(filepath, "w", "utf-8") as f:
        for i in range(topn):
            word, count = items2[i]
            f.write("{}:{}\n".format(word, count))


# 生成词频文件
wordFreq2("output/天龙八部词频_人名.txt", 300)

# 将txt文本里的数据转换为字典形式
fr = open('output/天龙八部词频_人名.txt', 'r', encoding='utf-8')
dic = {}
keys = []  # 用来存储读取的顺序
for line in fr:
    # 去空白,并用split()方法返回列表

    v = line.strip().split(':')

    dic[v[0]] = v[1]
    keys.append(v[0])
fr.close()
# 输出前几个的键值对
print("人物出现次数TOP", mainTop)
print(list(dic.items())[:mainTop])

# 　绘图
# 人名列表 (用于人物关系图,pyecharts人物出场次数图)
list_name = list(dic.keys())  # 人名
list_name_times = list(dic.values())  # 提取字典里的数据作为绘图数据


# 可视化人物出场次数
def creat_people_view():
    bar = Bar()
    bar.add_xaxis(list_name[0:keshihuaTop])
    bar.add_yaxis("人物出场次数", list_name_times,color='blue')
    bar.set_global_opts(title_opts=opts.TitleOpts(title="人物出场次数可视化图", subtitle="天龙八部人物TOP10"),
                        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}))
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))
    # bar.render_notebook()  # 在 notebook 中展示
    # make_snapshot(snapshot, bar.render(), "bar.png")
    # 生成 html 文件
    bar.render("output/天龙八部人物出场次数可视化图.html")


# 生成词云
def creat_wordcloud():
    bg_pic = imageio.imread('prepare/img.png')
    wc = wordcloud.WordCloud(font_path='c:\Windows\Fonts\simhei.ttf',
                             background_color='white',
                             width=1000, height=800,

                             max_words=500,
                             mask=bg_pic  # mask参数设置词云形状
                             )
    # 从单词和频率创建词云
    wc.generate_from_frequencies(counts2)
    # generate(text)  根据文本生成词云
    # wc.generate(txt)
    # 保存图片
    wc.to_file('output/天龙八部词云_人名.png')

    #  显示词云图片
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


# 使用pyecharts 的方法生成词云
def creat_wordcloud_pyecharts():
    wordsAndTimes = list(dic.items())
    (
        WordCloud()
            .add(series_name="人物次数", data_pair=wordsAndTimes,
                 word_size_range=[20, 100], textstyle_opts=opts.TextStyleOpts(font_family="cursive"), )
            .set_global_opts(title_opts=opts.TitleOpts(title="天龙八部词云"))
            .render("output/天龙八部词云_人名.html")
    )

# 颜色生成
colorNum = len(list_name[0:peopleTop])

# print('颜色数',colorNum)
def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color

def color_list():
    colorList = []
    for i in range(colorNum):
        colorList.append(randomcolor())
    return colorList

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签


# 生成人物关系图
def creat_relationship():
    # 人物节点颜色
    colors = color_list()
    Names = list_name[0:peopleTop]
    relations = {}
    # 按段落划分，假设在同一段落中出现的人物具有共现关系
    lst_para = (txt).split('\n')  # lst_para是每一段
    for text in lst_para:
        for name_0 in Names:
            if name_0 in text:
                for name_1 in Names:
                    if name_1 in text and name_0 != name_1 and (name_1, name_0) not in relations:
                        relations[(name_0, name_1)] = relations.get((name_0, name_1), 0) + 1
    maxRela = max([v for k, v in relations.items()])
    relations = {k: v / maxRela for k, v in relations.items()}
    # return relations

    plt.figure(figsize=(15, 15))
    # 创建无多重边无向图
    G = nx.Graph()
    for k, v in relations.items():
        G.add_edge(k[0], k[1], weight=v)
    # 筛选权重大于0.6的边
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.6]
    # 筛选权重大于0.3小于0.6的边
    emidle = [(u, v) for (u, v, d) in G.edges(data=True) if (d['weight'] > 0.3) & (d['weight'] <= 0.6)]
    # 筛选权重小于0.3的边
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.3]
    # 设置图形布局
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    # 设置节点样式
    nx.draw_networkx_nodes(G, pos, alpha=0.8, node_size=1300, node_color=colors)
    # 设置大于0.6的边的样式
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2.5, alpha=0.9, edge_color='g')
    # 0.3~0.6
    nx.draw_networkx_edges(G, pos, edgelist=emidle, width=1.5, alpha=0.6, edge_color='y')
    # <0.3
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.4, edge_color='b', style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=14)

    plt.title("《天龙八部》主要人物社交关系网络图")
    # 关闭坐标轴
    plt.axis('off')

    # 保存图表
    plt.savefig('output/《天龙八部》主要人物社交关系网络图.png', bbox_inches='tight')
    plt.show()


def main():

    #生成词频词性文件
    create_wordproperties()
    # 人物出场次数可视化图
    creat_people_view()

    # 词云图
    creat_wordcloud()
    creat_wordcloud_pyecharts()
    # 人物关系图
    creat_relationship()



if __name__ == '__main__':
    main()
