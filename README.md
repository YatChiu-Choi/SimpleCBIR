# SimpleCBIR
This is a curriculum design, a CBIR system with Python

这是我自学计算机视觉的时候，参考资料实现的一个基于内容的图像检索系统CBIR系统
包括提取Sift特征，利用机器学习K-means方法
完成将Sift特征向量聚类来生成图像词汇
。对词汇建索引，建立直方图向量，计算两个图像的相似度等

# 环境
1. 系统环境：Ubuntu 16.04
2. Python 2.7.12
3. 依赖库:
> cherrypy
> pickle
> PIL
> sicpy
> matplotlib
> pysqlite2
> urllib
> numpy
> （VLFEAT是命令行工具，在Python中使用OS库调用，可以到官方网站下载）
>> （以上包皆在linux下使用Pip安装）
4. 注意：拷贝到你的主机下时，请修改service.conf文件第9行为你在Ubuntu下的代码文件存在的绝对路径
## How to Run
1. 先下载图像数据集和配置好依赖库
2. 运行sift.py，提取sift特征
3. 运行vocabulary.py ，推提取好的特征进行聚类，构建图像直方图
4. 运行imagesearch.py，把得到的词汇文件，和图像一一对应起来，构建数据库，方便查找
5. 运行search.py ，然后打开命令行提示的网站（本地），就可以进行检索了。
7. 点击图像就可以进行检索（内部图例查询）
# 最后
检索的效果可能不够好，这是因为sift特征太简单了，你可以使用复杂一点的特征，例如图像金字塔的sift特征，或者卷积神经网络的特征
把送到聚类里面的特征修改，就能得到对应的检索效果

如果你有任何疑问：请咨询：YatChiu@foxmail.com 
2017 / 06 / 24
Samson Cai	
