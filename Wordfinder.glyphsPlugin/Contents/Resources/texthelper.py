#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import struct


def unichar(i):
    """
    A way to return unicode chars for the range above FFFF for "narrow python builds"
    Solution from https://stackoverflow.com/a/28326717/999162
    """
    try:  # Python 2
        return unichr(i)
    except NameError:  # Python 3
        return chr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')


def filterWritableWords(words, letters):
    """
    Filter out all words that cannot be written with the given letters
    Return List of words can be written with the given letters
    """
    containsSomeLetters = re.compile("[" + "".join(letters) + "]+", re.UNICODE)
    containsOtherLetters = re.compile("[^" + "".join(letters) + "]+", re.UNICODE)

    # very efficient way of determining if a word is made up entirely of the supplied
    # characters; fails fast if the word contains NO characters at all, and faster
    # second check with regex, compared to for .. in
    filtered = [w for w in words if containsSomeLetters.search(w) is not None and containsOtherLetters.search(w) is None]

    return filtered


def filterInterestWords(words, letters):
    """
    Filter out all words that don't contain any of the letters
    Return List of words that contain at least one of letters
    """
    containsSomeLetters = re.compile("[" + "".join(letters) + "]+", re.UNICODE)

    filtered = [w for w in words if containsSomeLetters.search(w) is not None]

    return filtered


def weightWords(words, letters):
    """
    Given a list of words and letters of interest
    Return List of each word's letter's weight
    The List is in same order of the words
    The List with the weights is the same order as the passed in letters
    Letters that don't occur in the word have 0 for that letter
    Example:
    words: [foo, bar, car]
    letters: [f, r]
    return: [[2.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]
    """
    weightedLetters = weightLetters(words, letters)

    weightedWords = []
    for word in words:
        wordLetterWeights = []
        for letter in letters:
            if letter in word:
                wordLetterWeights.append(weightedLetters[letter])
            else:
                wordLetterWeights.append(0)
        weightedWords.append(wordLetterWeights)

    return weightedWords


def weightLetters(words, letters):
    """
    Given a list of words and letters of interest count globally all letter
    occurrances
    Return Dict of { letter: occurrances } pairs
    """
    occurrances = {}
    for word in words:
        for letter in word:
            # if letter not in letters:
            #     continue

            if letter not in occurrances:
                occurrances[letter] = 1
            else:
                occurrances[letter] = occurrances[letter] + 1

    return occurrances
