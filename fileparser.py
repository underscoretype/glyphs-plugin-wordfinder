#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This is a helper script included in the Wordfinder Glyphs App plugin
to use for extracting sensible words from a text file passed in as
first argument
'''

import sys
import os
import re
import codecs


if (len(sys.argv) != 2):
	exit("Pass in the path to the file to parse, e.g. python fileparser.py text.txt will parse and create text-parsed.txt")

file = codecs.open(sys.argv[1], "r", "utf8")
text = file.read()

# remove punctuation marks
text = re.sub(r"[\d|\,|\.|\;|\:|\(|\)|\[|\]|\"|。|，|、|（|）]+", " ", text, 0, re.UNICODE)

# get rid of very plain latin ("ascii") words
text = re.sub(r"\b[a-zA-Z]{,5}\b", " ", text, 0, re.UNICODE)

# remove hyphens at word boundaries
text = re.sub(r"\s\-+|\-+\s", " ", text, 0, re.UNICODE)

# remove non-word strings
text = re.sub(r"\s\W+\s", " ", text, 0, re.UNICODE)

# split by spaces
li = re.split(r"\s+", text)

# make a list of unique words that are longer than one glyph
uniques = list(set([i for i in li if len(i) > 1]))
text = "\n".join(uniques)

filename = os.path.basename(os.path.splitext(sys.argv[1])[0]) + "-parsed.txt"

out = codecs.open(filename, "w", "utf8")
out.write(text)
out.close()

exit("Write %d unique words to %s" % (len(uniques), filename))
