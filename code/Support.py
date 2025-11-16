from csv import reader
from os import walk
import pygame
#用于读取CSV格式的关卡布局文件
# 将CSV文件中的数据转换为二维列表结构
# 每一行CSV数据都被转换为一个列表，整个文件形成一个包含多个行列表的地形地图(terrain_map)
def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

# 遍历指定路径下的所有图像文件
# 使用pygame加载每个图像文件并转换为Surface对象
def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list
