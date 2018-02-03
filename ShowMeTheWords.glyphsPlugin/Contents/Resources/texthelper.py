#!/usr/bin/python
# -*- coding: utf-8 -*-

def filterWritableWords(words, letters):
    """
    Filter out all words that cannot be written with the given letters
    Return List of words can be written with the given letters
    """
    filtered = []
    for word in words:
        writeable = True
        for letter in word:
            if letter not in letters:
                writeable = False
                break 
        if writeable:
            filtered.append(word)

    return filtered


def filterInterestWords(words, letters):
    """
    Filter out all words that don't contain any of the letters
    Return List of words that contain at least one of letters
    """
    filtered = []
    for word in words:
        interest = False
        for letter in word:
            if letter in letters:
                interest = True
        if interest:
            filtered.append(word)

    return filtered


def weightWords(words, letters):
    """
    Given a list of words and letters of interest
    Return List of each word's letter's weight
    The List is in same order or the words
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
    Return Dict of { letter: occurrances } paris
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

    # for letter, value in occurrances.items():
    #     occurrances[letter] = value / len(letters)

    return occurrances