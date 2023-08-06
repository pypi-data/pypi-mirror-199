#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2023/3/25 11:23
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""
import numpy as np


# 从file中读取配置信息
def read_conf(_config_file):
	conf = {}
	with open(_config_file, 'r') as f:
		for line in f:
			if line.startswith('#'):
				continue
			line = line.strip()
			if line == '':
				continue
			key, value = line.split('=')
			key = key.strip()
			value = value.strip()
			value = value.split('#')[0].strip()
			if value == '':
				continue
			value = char_to_logical(value)
			if value.startswith('['):
				value = value[1:-1].split(':')
				value = np.arange(float(value[0]), float(value[2]), float(value[1]))
			elif value.isdigit():
				value = float(value)
			conf[key] = value
	return conf


def char_to_logical(_str):
	# 不区分大小写比较
	if _str.lower() == '.true.':
		return True
	elif _str.lower() == '.false.':
		return False
	else:
		return _str
