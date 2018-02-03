#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, random, re, sys

from filereader import loadWords
from texthelper import filterWritableWords, filterInterestWords, weightWords


# keep a global record of words, so we don't need to reload them for each call
words = []


def getWords():
	"""
	Return List of words, from cache or load it
	"""
	global words
	if len(words) == 0:
		words = loadWords(os.path.dirname(os.path.realpath(__file__)) + "/words/")
		title = [word.capitalize() for word in words]
		caps = [word.upper() for word in words]
		
		words = words + title + caps

	return words


def wordfinder(available, required):
	"""
	Attempt to find the least amount of words spelled from the available 
	letters and using all required letters
	"""
	# make both input letters lists free of duplicates
	available = list(set(available))
	required = list(set(required))

	universe = getWords()
	print "dictionary total length", len(universe)

	# reduce a request for required by those letters not in available
	if not set(required).issubset(set(available)):
		illegal = set(required).difference(set(available))
		print "ILLEGAL", illegal, "required but not available"
		required = list(set(required).intersection(set(available)))

	# TODO output warning about available characters not in the universe
	
	print "required", required

	# TODO if required are all uppercase, transform universe

	universe = filterWritableWords(universe, available)
	print "dictionary writeable length", len(universe)

	universe = filterInterestWords(universe, required)
	print "dictionary relevant length", len(universe)

	words = []

	while len(required) > 0:
		wordsValues = weightWords(universe, required)
		# print wordsValues

		bestWordIndex = bestWord(wordsValues)
		if bestWordIndex == False:
			print "no match found"
			break

		word = universe[bestWordIndex]
		words.append(word)
		letters = list(set([letter for letter in word]).intersection(set(required)))
		print "word", word, "satisfies", letters
		del universe[bestWordIndex]
		print "req", len(required), required
		required = list(set(required).difference(set(letters)))
		print "req", len(required), required

	# print words
	print prettyList(words)
	print "end"


def bestWord(values):
	"""
	From a List of Lists with values
	Return the index of the word with the best values
	Greedy first: The List with most non-0 entries first
	Quality second: Of Lists with same number of entries, pick the one with 
	combined lowest value (rarest letters)
	Example:
	values: [[0,1,10], [0,0,2], [5, 2, 0]]
	greedy reduce to: [[0, 1, 10], [5, 2, 0]]
	quality score: [11, 7]
	return: 2 (index of [5, 2, 0] in values)
	"""
	matches = []
	num = 0
	for index, value in enumerate(values):
		relevant = len([count for count in value if count != 0])
		if relevant > num:
			matches = []
			num = relevant
		if relevant == num:
			matches.append({reduce(lambda x, y: x + y, value): index})

	# print "bestWords", num, matches
	if num == 0:
		print "No words with matches found"
		return False

	if matches:
		match = random.choice(matches)
		
		return match.values()[0]

	return False


def prettyList(li):
	return repr([x.encode(sys.stdout.encoding) for x in li]).decode('string-escape')


# testing on cli
if __name__ == "__main__":
	# get_words(10, [u"é", u"è", "a", "t", "s", "u", "i"])
	availableLetters = [ u"ß", u"ÿ", u"á", "a", "b", "c", "d", "e", "f", 
		"g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", 
		"u", "v", "w", "x", "y", "z", u"è", u"é", "A", "B", "C", "D", u"ä", u"ü"]
	# wordfinder(availableLetters, [u"q", u"u", u"t", u"l", u"o", u"x", "y", u"ß", "e", "a"])
	wordfinder(availableLetters, [u"ü", "z", u"è", u"é"])

	# strings = loadAllInDirectory(wordsDir)
	# availableLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]

	# strings = filter(strings, availableLetters, [u"a", u"b", u"c"])
	# # print strings
	
	# rated_words = word_rating(" ".join(strings))
	# print rated_words

	


