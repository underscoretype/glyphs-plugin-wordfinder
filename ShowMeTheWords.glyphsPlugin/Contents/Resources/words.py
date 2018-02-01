#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, random, re
from collections import OrderedDict
import texthelper

wordsFile = os.path.dirname(os.path.realpath(__file__)) + "/words/test.txt"
wordsDir = os.path.dirname(os.path.realpath(__file__)) + "/words/"
words = []


def load(path):
	if not os.path.isfile(path):
		return exit("No file to load")
	else:
		file = open(path, "r")
		txt = file.read().decode("utf-8")
	return txt


def loadAllInDirectory(directory, minLength = 3):
	string = ""
	words = []

	directorylist = os.listdir(directory)
	for file in directorylist:
		loaded = load(directory + file)
		if loaded:
			for part in re.compile("\s").split(loaded):
				if len(part) >= minLength:
					words.append(part)

	return words


# Filter the input text to what we need it
# 1) Filter down to only words that can be written with the font
# 2) Filter if an selection of must-include letters was passed in
def filter(words, availableLetters = False, requiredLetters = False):
	if not words:
		return False

	# remove duplicates
	words = list(set(words))

	if availableLetters:
		words = texthelper.filterWordsByGlyphs(words, availableLetters, requiredLetters, 3)

	return words




# pick all words writeable with given letters
# determine raretiy of letters
# give each word coverage value based on coveing the most rare letters
# traverse down the list of words sorted by coverage and calculate how many letters a word covers
# if no word covers all letters pick the word highest on the coverage list and find with next word with which is covers the highest amount of letters
# 	repeat until all letters are covered
def get_words(amount = 1, letters = False, availableLetters = False):
	text = loadAllInDirectory(wordsDir)
	words = []
	wordsRated = []
	wordsByLetters = {}

	if not text or not availableLetters or not letters:
		return

	# print text.find(u"ß")
	# print text[31450:31460]
	# filter the text to only include words that contain any of the
	# letters we are looking for, and can be written with the letters
	# available for writing
	text = filter(text, availableLetters, letters)

	# print text

	if not text:
		# no words were found that can be written with the available glyphs and contain 
		# any of the search glyphs
		# try if any words can be found that can partially be written, then sort them by
		# number of missing glyphs

		# print "no words with all glyphs and search"
		# text = loadAllInDirectory(wordsDir)
		# text = texthelper.wordsThatHaveAnyOf(text, letters)
		# print "words without glyphs but search"
		# print text
		# if not text:
		return exit("No fitting text could be found")

	print text

	# reduce duplicates
	text = list(set(text))


	wordsRated = rate_text(text)
	print wordsRated


	# is there a word that covers all letters?
	for ratedWord in wordsRated:
		if len(word_contains_letters(ratedWord.values()[0], letters)) == len(letters):
			print "found perfect match", ratedWord
			words.append(ratedWord)

	if len(words) == 0:
		# print "finding best combo", wordsRated
		satisfied = []
		while len(satisfied) < len(letters) and len(wordsRated) > 0:
			# print "satisfied", len(satisfied), "of", len(letters)
			# print "wordsRated", wordsRated, len(wordsRated)
			nextLeastCommonWord = wordsRated.pop(0).values()[0]
			lettersCoveredInWord = word_contains_letters(nextLeastCommonWord, letters)
			print "word", nextLeastCommonWord, "covers letters", lettersCoveredInWord
			# print "intersection with letters", letters, set(letters), list(set(letters).intersection(lettersCoveredInWord))
			satisfiedBefore = satisfied
			satisfied = list(set(satisfied + list(set(letters).intersection(lettersCoveredInWord))))
			# print "-words-", words
			if (len(satisfiedBefore) < len(satisfied)):
				words.append(nextLeastCommonWord)

				missing = [item for item in letters if item not in satisfied]
				plain_words = [item.values()[0] for item in wordsRated]

				# words = filter(words, availableLetters, missing)
				print "words after loop", len(plain_words)
				plain_words = texthelper.filterWordsByGlyphs(plain_words, availableLetters, missing, 3)
				plain_words = set(list(plain_words))
				print "words for new loop", len(plain_words)

				wordsRated = rate_text(plain_words)
				print len(wordsRated)
				print "satisfied", satisfied
				print "letters", letters
				print "missing", missing
				wordsRated = rate_text(plain_words, missing)
				# print "WORDSRATED", wordsRated
			else:
				print "word", nextLeastCommonWord, "only repeats already found letters"
			# print "next word", nextLeastCommonWord
			# print "now covering", satisfied, "of required", letters

			# print "rating words again"
			# print [item.values()[0] for item in wordsRated]



	print "found", words
	# r = []

	# if (len(words) < amount):
	# 	for word in words:
	# 		print "WORD", word
	# 		r.append(word)
	# else:
	# 	while (len(r) < min(amount, len(words))):
	# 		word = random.choice(words)
	# 		if word not in r:
	# 			r.append(word)
			
	# print "return", r
	# return r

# Rate a list of words by their internal letter commonness
# Look at all words and all letters and count their occorances
# to determine what are words made up of "rare" letters
#
# Return a list of dicts of word-rareness to word
#
# If passing in glyphs, only take those glpyhs into account
# for calculating the rareness of a word
def rate_text(text, glyphs = False):
	wordsRated = []
	wordsByLetters = word_rating(text, glyphs) # dict of u"x": [words, ]

	# print "WORDS BY LETTERS", wordsByLetters

	wordsByLettersCounted = {k: f(v) for k, v in wordsByLetters.iteritems()} # dict of u"x": count
	letterFrequenciesSorted = sorted(wordsByLettersCounted.items(), key=lambda x: x[1]) # list oftuples of (u"x", count) sorted by count
	letterFrequencies = dict(letterFrequenciesSorted) # the lower the rarer

	# print letterFrequencies
	# print glyphs

	for word in text:
		commonness = 0.0 # the lower the rarer
		for letter in word:
			if glyphs == False or (glyphs != False and letter in glyphs):
				commonness = commonness + letterFrequencies[letter]
		commonness = commonness / len(word)
		wordsRated.append( {commonness: word })#, len(list(set))) )
		# print "word", word, "commonness", commonness, "number of unique letters", len(list(set(word)))

	wordsRated = sorted(wordsRated) # automatically sorts by the list items (dict's) commonness keys
	# print wordsRated
	return wordsRated


def f(item):
	return len(item)


def word_contains_letters(word, letters):
	found = []
	for letter in word:
		if letter in letters and letter not in found:
			found.append(letter)
	return found


def word_rating(words, glyphs = False):
	wordsByLetters = {}
	for word in words:
		registeredWordLetters = []
		for letter in word:
			if letter != "\n" and letter not in registeredWordLetters:
				if glyphs == False or (glyphs != False and letter in glyphs):
					if letter not in wordsByLetters:
						wordsByLetters[letter] = []
					
					wordsByLetters[letter].append(word)
					registeredWordLetters.append(letter)

	for key in wordsByLetters.keys():
		print "key", key, "num words", len(wordsByLetters[key])

	return wordsByLetters


# testing on cli
if __name__ == "__main__":
	# get_words(10, [u"é", u"è", "a", "t", "s", "u", "i"])
	availableLetters = [u"ß", u"ÿ", u"á", u"", "2", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]
	get_words(1, [u"q", u"u", u"t", u"l", u"o", u"x"], availableLetters)

	# strings = loadAllInDirectory(wordsDir)
	# availableLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]

	# strings = filter(strings, availableLetters, [u"a", u"b", u"c"])
	# # print strings
	
	# rated_words = word_rating(" ".join(strings))
	# print rated_words

	


