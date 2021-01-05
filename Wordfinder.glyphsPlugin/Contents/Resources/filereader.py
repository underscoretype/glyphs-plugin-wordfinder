#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, re
from io import open

def load(path):
	"""
	Simple file loader with checks
	Return String of file content
	"""
	if not os.path.isfile(path):
		return False
	else:
		file = open(path, "r", encoding="utf8")
		txt = file.read()
	return txt


def loadWords(directory):
	"""
	Load all words from all files in given directory
	Return List of words
	"""
	words = []
	directorylist = os.listdir(directory)
	for file in directorylist:
		try:
			loaded = load(directory + file)
			if loaded:
				for part in re.compile("\s").split(loaded):
					words.append(part)
		except:
			words = words

	return words