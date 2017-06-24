# coding=utf-8
# vacabulary.py
#
'''
	创建一个词汇类
	根据提取都的特征，使用 K-Means 聚类构建图像词汇

'''

from numpy import *
from scipy.cluster.vq import *  # 使用vq里面的kmeans函数，进行聚类
import sift  # 提取sift特征
import generate_imlist
import pickle

class Vocabulary(object):
	"""提取图像词汇，创建词汇本"""

	def __init__(self, name):

		self.name = name  #
		self.voc = []  # 由单词聚类中心VOC与每个单词对应的逆向文档频率构成的向量
		self.idf = []  # 逆向文档频率
		self.trainingdata = []  # trainingdata应改为trainngData增加易读性
		self.nbr_words = 0  # nbr_words图片的个数

	# -----------初始化结束---------------------------

	def train(self, featurefiles, k=100, subsampling=10):
		'''
			用含义k个单词的K-means列出在featurefiles 中的特征文件训练出一个词汇。
			对训练数据下采样可以加快训练速度
		'''
		nbr_images = len(featurefiles)  # 图像特征文件的个数
		# 从文件中读取特征
		descr = []  # descr<-description的缩写，也就是描述子
		descr.append(sift.read_features_from_file(featurefiles[0])[1]) # 添加描述子
		descriptors = descr[0]  # 将所有的特征并在一起，以便后面进行K-means聚类
		print '训练中数据...请稍等'
		for i in arange(1, nbr_images):
			descr.append(sift.read_features_from_file(featurefiles[i])[1])
			
			descriptors = vstack((descriptors, descr[i]))
		# ------------读取特征结束----------------

		# K-means：最后一个参数决定运行次数,
		# 此处可以调整kmeans的参数来进行优化
		self.voc, distortion = kmeans(descriptors[::subsampling, :], k, 1)  # 有问题
		self.nbr_words = self.voc.shape[0]  # ???获得第一维

		# 遍历所有的训练图像，并投影到词汇上
		imwords = zeros((nbr_images, self.nbr_words))
		for i in range(nbr_images):
			imwords[i] = self.project(descr[i])

		nbr_occurences = sum((imwords > 0) * 1, axis=0)  # axis=0,求范数0和

		self.idf = log((1.0 * nbr_images) / (1.0 * nbr_occurences + 1))
		self.trainingdata = featurefiles
		print '训练结束'

	def project(self, descriptors):
		'''将描述子投影到词汇上，以创建单词直方图'''

		# 图像单词直方图image_histogram
		imhist = zeros((self.nbr_words))
		words, distance = vq(descriptors, self.voc)  # vq是什么函数？

		for w in words:
			imhist[w] += 1
		return imhist  # imhist单词的直方图


	def get_words(self, descriptors):
		""" Convert descriptors to words. """
		return vq(descriptors, self.voc)[0]


if __name__ == '__main__':
	# 提取特征与训练词汇
	data_set_path = 'holidaytest'
	imlist = generate_imlist.generate_imlist(data_set_path)
	featlist = generate_imlist.generate_sift(data_set_path)


	comfirm = input('请确认是否训练词汇，是请输入1：')

	if comfirm == 1:
		# 存取图像数据集的路径
		
		voc = Vocabulary(data_set_path)
		voc.train(featlist, 1000, 10)

		# 使用pickle库，这样格式能比较友好保存词汇
		with open('Voc.pkl', 'wb') as f:
			pickle.dump(voc, f)
		print 'vocabulary is:', voc.name, voc.nbr_words
