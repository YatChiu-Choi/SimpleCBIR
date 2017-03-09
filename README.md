# SimpleCBIR
This is a curriculum design, a CBIR system with Python

这是我自学计算机视觉的时候，完成的基于内容的CBIR系统，作为我Python语言课程的课程设计
包括提取Sift特征，利用机器学习K-means方法完成将Sift特征向量聚类来生成图像词汇。对词汇建索引，建立直方图向量，计算两个图像的相似度

1.系统环境：Ubuntu 16.04
2.Python 2.7.12
3.依赖库:
	cherrypy
	pickle
	PIL
	sicpy
	matplotlib
	pysqlite2
	urllib
	numpy
	（VLFEAT是命令行工具，在Python中使用OS库调用）
	（以上包皆在linux下使用Pip安装）
4.注意：拷贝到你的主机下时，请修改service.conf文件第9行为你在Ubuntu下的代码文件存在的绝对路径
5.预处理已经完成，打开运行search.py文件即可。
6.如果你有任何疑问：请咨询：416550695@qq.com ,Samson Cai	
