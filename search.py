#coding=utf-8


import cherrypy, os, urllib, pickle
import imagesearch
import random
import generate_imlist
import vocabulary
class WebService(object):
	def __init__(self):
		# 载入图像列表

		self.imlist = generate_imlist.generate_imlist()
		self.featlist= generate_imlist.generate_sift()

		self.nbr_images = len(self.imlist)
		self.ndx = range(self.nbr_images)

		# 载入词汇表
		#with open('vocabulary.pkl', 'rb') as f:
		# 	self.voc = pickle.load(f)
		voc = vocabulary.Vocabulary('ukbenchtest')
		voc.train(self.featlist, 1000, 10)

		# 设置可以显示多少幅图像
		self.maxres = 30  # 30幅


		# html 的头部和尾部x
		self.header = """
		<!doctype html>
		<head>
		<title>Image search example</title>
		</head>
		<body>
		"""
		self.footer = """
		</body>
		</html>
		"""

	def index(self, query=None):

		self.src = imagesearch.Searcher('web.db', self.voc)

		html = self.header
		html += """
		<br />
		Click an image to search. <a href='?query='>Random selection</a> of images.
		<br /><br />
		"""

		if query:
			# 查询数据库并获取靠前的图像
			res = self.src.query(query)[:self.maxres]
			for dist, ndx in res:
				imname = self.src.get_filename(ndx)
				html += "<a href='?query=" + imname + "'>"
				html += "<img src='" + imname + "' width='100' />"
				html += "</a>"
		else:
			# 如果没有查询图像,则显示随机选择的图像
			random.shuffle(self.ndx)
			for i in self.ndx[:self.maxres]:
				imname = self.imlist[i]
				html += "<a href='?query=" + imname + "'>"
				html += "<img src='" + imname + "' width='100' />"
				html += "</a>"
			html += self.footer

		return html

	index.exposed = True  #此方法可以被发布

cherrypy.quickstart(WebService(),'/',config=os.path.join(os.path.dirname(__file__), 'service.conf'))
# '/',
#cherrypy.q