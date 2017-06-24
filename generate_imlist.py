# coding=utf-8

import os


def generate_imlist(dataset_path):
	'param: dataset_path存放图像数据的路径'
	dir = os.getcwd()
	# 返回图像库里面的文件名字
	'''
	for root,dirs,files in os.walk(dir+dataset_path):

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


def generate_sift(dataset_path):
	image_list = generate_imlist(dataset_path)
	sift_list = []
	for names in image_list:
		# 把对应的图像名字的后缀改为sift，图像和特征一一对应比较有利于后续工作
		type = 'JPG'
		sift_list.append(names.replace(type, 'sift'))

	return sift_list
