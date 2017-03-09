# coding=utf-8

import os


def generate_imlist():
	dir = os.getcwd()
	# 返回图像库里面的文件名字
	'''
	for root,dirs,files in os.walk(dir+'/ukbench_test'):

		for file in files:

			imagename=os.path.join(root,file)
			

			imlist.append(imagename)
	return imlist
	'''
	imageLibrary = '/ukbench_test'  # 存放图像的目录
	items = os.listdir(dir + imageLibrary)
	image_list = []
	for names in items:
		if names.endswith(".JPG"):
			image_list.append(imageLibrary + names)

	return image_list


def generate_sift():
	image_list = generate_imlist()
	sift_list = []
	for names in image_list:
		sift_list.append(names.replace('JPG', 'sift'))

	return sift_list