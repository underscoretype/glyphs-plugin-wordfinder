#!/usr/bin/python
# -*- coding: utf-8 -*-

# built-in modules
import operator

# dependency modules
import regex


def removePunctuation(text):
    return regex.sub(ur"\p{P}+", "", text)


def removeNumbers(text):
    return regex.sub(ur"\d+", "", text)


# Remove any word that includes other than the passed in glyphs, i.e. can't
# be written
def filterWordsByGlyphs(words, glyphs, inWord = False, minWordLength = 5):
    print "filter words made up of glyphs", glyphs
    print "containing any of", inWord
    print "min length", minWordLength
    if not words:
        return False

    if not glyphs:
        return words

    print glyphs

    print "WORDS", words

    filtered = []
    for word in words:
        if word is "" or len(word) < minWordLength:
            continue

        validWord = True
        for letter in word:
            if letter not in glyphs:
                # print letter, "not in glyphs"
                validWord = False
                break

        if validWord and word:

            if inWord:

                #additionally check if this word has any of the required inWord letters
                for letter in word:
                    if letter in inWord:
                        filtered.append(word)
            else:

                # otherwise just allow this word
                filtered.append(word)

    return filtered


def wordsThatHaveAnyOf(words, glyphs, minWordLength = 5):
    filtered = []
    for word in words:
        # print word
        # if word is "" or len(word) < minWordLength:
        #     continue

        for glyph in glyphs:
            # print glyph, word
            if glyph in word:
                filtered.append(word)
                break

    return filtered


# Reduce any duplicates from the input text (if it was natural text, as opposed to a dictionary)
# From https://www.peterbe.com/plog/uniqifiers-benchmark
# Not order preserving
def removeDuplicates(text):
    keys = {}
    for e in text:
        keys[e] = 1
    text = keys.keys()

    return text
