# coding=utf-8

from PIL import Image
#from pysqlite2 import dbapi2 as sqlite
import sqlite3
import sift
from pylab import *
import generate_imlist
import pickle
import vocabulary


class Indexer(object):

	"""
	这个类是用来给图片已经对应词汇直方图建立索引
	"""

	# 为图片创建索引的类
	def __init__(self,db,voc):

		self.con=sqlite3.connect(db)  # 连接数据库
		self.voc=voc   # 图像词汇表

	def __del__(self):
		#
		self.con.close()  # 关闭数据库连接



	def db_commit(self):
		# 提交到数据库
		self.con.commit()

	def create_tables(self):
		# 以下均为数据库操作，建表
		self.con.execute('create table imlist(filename)')
		self.con.execute('create table imwords(imid,wordid,vocname)')
		self.con.execute('create table imhistograms(imid,histogram,vocname)')
		self.con.execute('create index im_idx on imlist(filename)')
		self.con.execute('create index wordid_idx on imwords(wordid)')
		self.con.execute('create index imid_idx on imwords(imid)')
		self.con.execute('create index imidhist_idx on imhistograms(imid)')
		self.db_commit()  #将变动的更改提交


	def add_to_index(self,imname,descr):
		"""获取带有特征描述子的图像，投影到词汇并添加进数据库"""
		if self.is_indexed(imname):
			#如果图像被标记索引了就返回
			return

		# 提示信息： 建立索引中
		print 'indexing',imname

		# 获取词汇的id号
		imid=self.get_id(imname)

		# 通过对描述子投射，获取图像的对应词汇
		imwords=self.voc.project(descr)
		nbr_words=imwords.shape[0]  # 获得词汇的个数

		for i in range(nbr_words):
			# 将每个单词连接起来，组成一个向量。
			word=imwords[i]

			# 数据库插入操作
			self.con.execute('insert into imwords(imid,wordid,vocname) values(?,?,?)',(imid,word,self.voc.name))

		# 存储图像的直方图
		# 用pickle模块将Numpy数组编码成字符串，存储起来
		self.con.execute("insert into imhistograms(imid,histogram,vocname) values(?,?,?)",(imid,pickle.dumps(imwords),self.voc.name))

	def is_indexed(self,imname):
		"""如果图像的名字被索引到了，就返回true"""
		#数据库操作
		im=self.con.execute("select rowid from imlist where filename='%s'"%imname).fetchone()

		return im!=None

	def get_id(self,imname):
		"""获取图像的id，如果不存在，就添加"""
		# 创建游标cursor
		cur=self.con.execute("select rowid from imlist where filename='%s'"%imname)

		res=cur.fetchone()

		if res==None:
			cur=self.con.execute("insert into imlist(filename) values('%s')"%imname)
			return cur.lastrowid
		else:
			return res[0]  #res是游标fetch回来的

class Searcher(object):
	# 这个类是用来对输入图片进行检索的
	def __init__(self,db,voc):
		#初始化数据库
		self.con=sqlite3.connect(db,check_same_thread=False)  # 连接到数据库
		self.voc=voc  # 提取词汇表

	def __del__(self):
		self.con.close()


	def candidates_from_word(self,imword):
		"""G获取包含imword的图像列表"""
		im_ids=self.con.execute('select distinct imid from imwords where wordid=%d'%imword).fetchall()

		# 获取候选图像
		candidates=[ i[0] for i in im_ids]
		return candidates


	def candidates_from_histogram(self,imwords):
		"""获取具有相似单词的图像列表"""
		#获取单词id
		words=imwords.nonzero()[0] #单词ID
		#寻找候选图像
		candidates=[]
		for word in words:
			c=self.candidates_from_word(word)
			candidates+=c
		#获取所有唯一的单词，并按照出现次数反向排序
		tmp=[(w,candidates.count(w)) for w in set(candidates)]
		tmp.sort(cmp=lambda x,y:cmp(x[1],y[1]))  #lambda
		tmp.reverse()

		#返回排序后的列表，匹配度最高的排在前面
		return [w[0] for w in tmp]

	def get_histogram(self,imname):
		"""返回一幅图像的单词直方图"""
		im_id = self.con.execute(" select rowid from imlist where filename='%s'"%imname).fetchone()

		s = self.con.execute("select histogram from imhistograms where rowid='%d'"%im_id).fetchone()
		#用pickle模块从字符串解码NUmpy数组
		#字符串和numpy数组的转换
		return pickle.loads(str(s[0]))

	def query(self,imname):
		# 查询方法
		# 查找所有与输入图像 匹配的图像列表

		h=self.get_histogram(imname)  # 获取输入图像的词汇直方图


		candidates=self.candidates_from_histogram(h) # 通过直方图得到候选图像

		matchscores=[] # 检索匹配结果的得分情况

		for imid in candidates:
			# 获取每个候选图像的名字
			cand_name=self.con.execute("select filename from imlist where rowid=%d"%imid).fetchone()

			# 获取候选图像的词汇直方图
			cand_h=self.get_histogram(cand_name)

			#   -------------------------------------
			# 把词汇直方图看作向量，计算两个向量的相似性
			cand_dist=sqrt( sum( self.voc.idf * dot((h-cand_h) ,(h-cand_h))**2 )) #用L2距离度量相似性，array的函数，对应元素相成再加
			#cand_dist = sqrt(sum(self.voc.idf * (multiply(h - cand_h,h-cand_h) ** 2)))

			#--------------------可改用其他方法改进

			matchscores.append( (cand_dist,imid) )

			#返回排序后的距离以及对应的ids列表
		matchscores.sort() # 对结果排序，计算的距离越小。相似度越大
		return matchscores

#----------------Search类结束---------------------
	def get_filename(self, imid):
		""" 返回图像 id 对应的文件名 """

		s = self.con.execute(
			"select filename from imlist where rowid='%d'" % imid).fetchone()
		return s[0]




def plot_results(src,res):
	""" 显示在列表 res 中的图像 """
	figure()
	nbr_results = len(res)
	for i in range(nbr_results):
		imname = src.get_filename(res[i])
		subplot(1,nbr_results,i+1)
		imshow(array(Image.open(imname)))
		axis('off')
	show()


if __name__ == '__main__':
	
	dataset_path = 'xxx'
	imlist = generate_imlist.generate_imlist(dataset_path)
	featlist = generate_imlist.generate_sift(dataset_path)
	
	# number of images
	nbr_images = len(imlist)
	
	# 图像集的路径
	dataset_path = 'holidaytest'
	# 载入词汇
	#voc = vocabulary.Vocabulary(dataset_path)
	# voc.train(featlist, 1000, 10)
	with open('vocabulary.pkl', 'rb') as f:
		voc = pickle.load(f)
	
	# 创建索引器
	database_name = 'test.db' # 将生成这个数据库文件
	indx = Indexer(database_name, voc)
	# 创建数据库表
	indx.create_tables()

	# 遍历整个图像库,将特征投影到词汇上并添加到索引中
	for i in range(nbr_images):
		locs, descr = sift.read_features_from_file(featlist[i])
		indx.add_to_index(imlist[i], descr)

	# 提交到数据库
	indx.db_commit()
	



