import os, re

def load(path):
	"""
	Simple file loader with checks
	Return String of file content
	"""
	if not os.path.isfile(path):
		return exit("No file to load")
	else:
		file = open(path, "r")
		txt = file.read().decode("utf-8")
	return txt


def loadWords(directory):
	"""
	Load all words from all files in given directory
	Return List of words
	"""
	words = []
	directorylist = os.listdir(directory)
	for file in directorylist:
		loaded = load(directory + file)
		if loaded:
			for part in re.compile("\s").split(loaded):
				words.append(part)

	return words