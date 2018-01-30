#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, random, re
from collections import OrderedDict
import text

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

	directorylist = os.listdir(directory)
	for file in directorylist:
		loaded = load(directory + file)
		if loaded:
			for part in loaded.split(" "):
				if len(part) >= minLength:
					string = string + "\n" + part

	return string


# Filter the input text to what we need it
# 1) Filter down to only words that can be written with the font
# 2) Filter if an selection of must-include letters was passed in
def filter(txt, requiredLetters = False, wordMinLength = False):
	if not txt:
		return False

	words = re.compile("\s").split(txt)

	# TODO remove duplicated (in case the corpus has any)
	if requiredLetters:
		words = text.filterWordsByGlyphs(words, requiredLetters, wordMinLength)

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

	# filter the text to only include words that contain any of the
	# letters we are looking for, and can be written with the letters
	# available for writing
	text = filter(text, availableLetters, letters)

	if not text:
		return exit("No fitting text could be found")

	# reduce duplicates
	text = list(set(text))

	wordsByLetters = word_rating(text) # dict of u"x": [words, ]
	wordsByLettersCounted = {k: f(v) for k, v in wordsByLetters.iteritems()} # dict of u"x": count
	letterFrequenciesSorted = sorted(wordsByLettersCounted.items(), key=lambda x: x[1]) # list oftuples of (u"x", count) sorted by count
	letterFrequencies = dict(letterFrequenciesSorted) # the lower the rarer

	print letterFrequencies

	for word in text:
		commonness = 0.0 # the lower the rarer
		for letter in word:
			commonness = commonness + letterFrequencies[letter]
		commonness = commonness / len(word)
		wordsRated.append( {commonness: word })#, len(list(set))) )
		# print "word", word, "commonness", commonness, "number of unique letters", len(list(set(word)))

	wordsRated = sorted(wordsRated) # automatically sorts by the list items (dict's) commonness keys
	print wordsRated


	# is there a word that covers all letters?
	for ratedWord in wordsRated:
		if len(word_contains_letters(ratedWord.values()[0], letters)) == len(letters):
			print "found perfect match", ratedWord
			words.append(ratedWord)

	if len(words) == 0:
		print "finding best combo", wordsRated
		satisfied = []
		while (len(satisfied) < len(letters)):
			nextLeastCommonWord = wordsRated.pop(0).values()[0]
			lettersCoveredInWord = word_contains_letters(nextLeastCommonWord, letters)
			# print "word", nextLeastCommonWord, "covers letters", lettersCoveredInWord
			# print "intersection with letters", letters, set(letters), list(set(letters).intersection(lettersCoveredInWord))
			satisfiedBefore = satisfied
			satisfied = list(set(satisfied + list(set(letters).intersection(lettersCoveredInWord))))
			if (satisfiedBefore < satisfied):
				words.append(nextLeastCommonWord)
			else:
				print "word", nextLeastCommonWord, "only repeats already found letters"
			# print "next word", nextLeastCommonWord
			# print "now covering", satisfied, "of required", letters


	print "found", words
	r = []

	if (len(words) < amount):
		for word in words:
			r.append(word.values()[0])
	else:
		while (len(r) < min(amount, len(words))):
			word = random.choice(words)
			if word not in r:
				r.append(word.values()[0])
			
	print "return", r
	return r


def f(item):
	return len(item)


def word_contains_letters(word, letters):
	found = []
	for letter in word:
		if letter in letters and letter not in found:
			found.append(letter)
	return found


def word_rating(words):
	wordsByLetters = {}
	for word in words:
		registeredWordLetters = []
		for letter in word:
			if letter != "\n" and letter not in registeredWordLetters:
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
	availableLetters = ["2", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]
	get_words(10, [u"a", u"n"], availableLetters)

	# strings = loadAllInDirectory(wordsDir)
	# availableLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]

	# strings = filter(strings, availableLetters, [u"a", u"b", u"c"])
	# # print strings
	
	# rated_words = word_rating(" ".join(strings))
	# print rated_words

	


