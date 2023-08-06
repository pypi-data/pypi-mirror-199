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
import contextlib

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
			conf[key] = value
	return conf


def char_to_logical(_str):
	# 不区分大小写比较
	if _str.lower() == '.true.':
		return True
	elif _str.lower() == '.false.':
		return False
	else:
		if _str.startswith('['):
			_str = _str[1:-1].split(',')
			for i in range(len(_str)):
				if is_number(_str[i]):
					_str[i] = float(_str[i])
				else:
					tmp_1 = _str[i].strip().split(':')
					_str[i] = np.arange(float(tmp_1[0]), float(tmp_1[2]) + float(tmp_1[1]), float(tmp_1[1])).tolist()
			_str = flatten_list(_str)
		elif _str.isdigit():
			_str = float(_str)
		return _str


def is_number(s):
	with contextlib.suppress(ValueError):
		float(s)
		return True
	with contextlib.suppress(TypeError, ValueError):
		import unicodedata  # 处理ASCii码的包
		unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
		return True
	return False


def flatten_list(_lst, flattened_list = []):
	# sourcery skip: default-mutable-arg
	for item in _lst:
		if isinstance(item, list):
			flatten_list(item)
		else:
			flattened_list.append(item)
	return flattened_list
