# coding=utf-8
# sift.py
from PIL import Image
from pylab import *
import os
import generate_imlist


'''提取sift特征'''


def process_image(imagename,resultname,params="--edge-thresh 10 --peak-thresh 5"):#第三个参数应该是命令行的参数
	"""处理一一幅图像，结果保存为pgm格式"""
	if imagename[-3:]!='pgm':
		# sift提取处理只能真多pmg格式，若图像的后缀不是.pmg,则转换格式
		im=Image.open(imagename).convert('L')   ##打开并且转换为灰度图
		im.save('tmp.pgm')  ##保存起来，tmp.pgm

	# 调用VLFeat的命令行
	# '/home/bigger/PycharmProjects/yat/glnxa64/sift '注意：这里用绝对路径！
	sift_path = '/home/bigger/PycharmProjects/yat/glnxa64/sift '  # vlfeat的sift文件所在路径
	cmmd = str(sift_path + 'tmp.pgm' + ' --output=' + resultname + ' ' + params)

	#把参数以字符串传送到命令行，调用vlfeat的命令行接口
	os.system(cmmd)  # sift

	print 'processed', imagename,'to' ,resultname


def read_features_from_file(filename):
	"""读取特征属性值，然后以矩阵形式返回"""
	#加载
	f=loadtxt(filename)  #numpy库的函数

	#f[:,:4]是属性的矩阵，f[:,4:]是128维向量的矩阵
	return f[:,:4],f[:,4:]#特征位置，描述子


def write_features_to_files(filename,locs,desc):
	#把修改的特征写进文档并保存
	#三个参数：文件名，位置,描述子
	savetxt(filename,hstack((locs,desc)))
	#hstack函数，拼接不同行向量，实现水平堆叠两个向量的功能
	#也就是实现一维拼接

#读取特征后，可以在图像上描绘他们的位置

def plot_features(im,locs,circle=False):
	"""显示带有特征的图像输入：im(数组图像d)，loc,每个特征的位置信息:行，列，尺度，朝向"""

	def draw_cicle(c,r):
		t=arange(0,1.01,.01)*2*pi
		x=r*cos(t)+c[0]
		y=r*sin(t)+c[1]
		plot(x,y,'b',linewidth=2)
		imshow(im)


	if circle:
		for p in locs:
			draw_cicle(p[:2],p[2])
	else:
		plot(locs[:,0],locs[:,1],'ob')
	axis('off') # 关闭坐标



if __name__ == '__main__':
	# 提取特征与训练词汇
	
	# 获取图像的路径列表和特征文件的路径列表
	imlist = generate_imlist.generate_imlist()
	featlist = generate_imlist.generate_sift()  

	comfirm = input('请确认是否提取特征，是请输入1：')

	if comfirm == 1:
		nbr_images = len(imlist)

		for i in range(nbr_images):
			process_image(imlist[i] , featlist[i])
		print '提取sift特征完毕'
