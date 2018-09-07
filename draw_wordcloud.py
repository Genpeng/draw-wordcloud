# _*_ coding: utf-8 _*_

"""
绘制比亚迪广告门事件词云图

Author: StrongXGP (xgp1227@gmail.com)
Date:	2018/09/07
"""

import os
import re
import jieba
import multidict
import numpy as np
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from time import time
from wordcloud import WordCloud


def load_data(data_path):
	text = list()
	with open(data_path, 'r', encoding='utf-8') as fin:
		lines = fin.read().splitlines()
		for line in lines:
			text.extend(line.split('\t'))
	return text


def load_stopwords(stopwords_path):
	with open(stopwords_path, 'r', encoding='utf-8') as fin:
		lines = fin.read().splitlines()
		stopwords = [line.strip().lower() for line in lines]
		stopwords = set(stopwords)
	return stopwords


def get_frequency_dict(data, stopwords=set()):
	full_terms_dict = multidict.MultiDict()
	temp_dict = {}

	for text in data:
		text = text.strip().lower()
		words = list(jieba.cut(text))
		for word in words:
			if word not in stopwords:
				freq = temp_dict.get(word, 0)
				temp_dict[word] = freq + 1

	for key in temp_dict:
		full_terms_dict.add(key, temp_dict[key])

	return full_terms_dict


def main():
	# 1. 载入数据
	# =========================================================================

	print("[INFO] Load data...")
	data_path = "text.txt"
	data = load_data(data_path)
	print("[INFO] Load finished!")

	# 2. 加载停用词
	# =========================================================================
	
	print("[INFO] Load stopwords...")
	stopwords_path = "stopwords.txt"
	stopwords = load_stopwords(stopwords_path)
	print("[INFO] Load finished!")

	# 3. 统计词频
	# =========================================================================

	print("[INFO] Count word frequency...")
	t0_count = time()
	full_terms_dict = get_frequency_dict(data, stopwords)
	print("[INFO] Done in %.3f seconds!" % (time() - t0_count))
	print("[INFO] Count finished!")

	# 4. 绘制词云图
	# =========================================================================

	font_path = "SourceHanSerifK-Light.otf"
	wc = WordCloud(font_path=font_path, width=1000, height=860, background_color='white')
	wc.generate_from_frequencies(full_terms_dict)

	plt.imshow(wc, interpolation='bilinear')
	plt.axis('off')
	plt.show()

	wordcloud_path = "wordcloud.png"
	wc.to_file(wordcloud_path)


if __name__ == '__main__':
	main()
