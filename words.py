import os, random, re
import text

wordsFile = "words/test.txt"
wordsDir = "words/"
words = []


def load(path):
	if not os.path.isfile(path):
		return exit("No file to load")
	else:
		file = open(path, "r")
		txt = file.read().decode("utf-8")
	return txt


def loadAllInDirectory(directory):
	text = ""

	directorylist = os.listdir(directory)
	for file in directorylist:
		loaded = load(directory + file)
		if loaded:
			text = text + "\n" + loaded

	return text


# Filter the input text to what we need it
# 1) Filter down to only words that can be written with the font
# 2) Filter if an selection of must-include letters was passed in
def filter(txt, requiredLetters = False, wordLetters = False):
	if not txt:
		return False

	words = re.compile("\s").split(txt)

	# TODO remove duplicated (in case the corpus has any)
	if requiredLetters:
		words = text.filterWordsByGlyphs(words, requiredLetters, wordLetters)

	return words


def get_words(amount = 1, letters = False):
	# text = load(wordsFile)
	text = loadAllInDirectory(wordsDir)

	filterLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	text = filter(text, filterLetters, letters)

	if not text:
		return exit("No fitting text could be found")

	words = []
	amount = min(len(text), amount)

	if amount == 0:
		print("not enough words found")
		return

	while (len(words) < amount):
		word = random.choice(text)
		if word not in words:
			words.append(word)

	print(words)

# testing on cli
if __name__ == "__main__":
	get_words(10, ["x", "y", "z"])


