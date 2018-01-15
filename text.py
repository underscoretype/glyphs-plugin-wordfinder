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
    if not words:
        return False

    if not glyphs:
        return words

    print glyphs

    filtered = []
    for word in words:
        if word is "" or len(word) < minWordLength:
            continue

        validWord = True
        for letter in word:
            if letter not in glyphs:
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


# Reduce any duplicates from the input text (if it was natural text, as opposed to a dictionary)
# From https://www.peterbe.com/plog/uniqifiers-benchmark
# Not order preserving
def removeDuplicates(text):
    keys = {}
    for e in text:
        keys[e] = 1
    text = keys.keys()

    return text
