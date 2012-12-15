#!/usr/bin/python

from __future__ import print_function
from sys import argv
import codecs
import re

BLOCKSIZE = 1048576 # 1 MB text buffer

def Unique(seq):
    """Returns unique elements from a list without changing order."""
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            yield item

def GetEntries(word, dic):
    """Combs dictionary for lines containing specified word.
       Returns a list of unique semicolon separated entries from those lines."""

    entries = [line.rstrip("\n\r") for line in dic if re.search(";%s;" % (word), line)]

    entries = [word for line in entries for word in line.split(";") if word]

    entries[:] = Unique(entries)

    if not entries:
        entries = [word]

    return entries

def ExtractKeywords(question, dic, dic2):
    """Returns a list of X, Y and Z synonyms and their inflections
       from a given question string, expects "Kto X Y w Z?" format."""

    synonyms = [ [] , [] , [] ]
    weights = [ 60, 30, 20 ]

    match = re.search("Kto (.+) (.+) w (.+)\?", ReplaceDiacritics(question))
    result = dict()

    if match:
        keywords = [GetEntries(word, dic)[0] for word in match.group(1,2,3)]
        keywords_and_synonyms = [GetEntries(word, dic2) for word in keywords]

        for x in range(len(keywords_and_synonyms)):
            if not keywords_and_synonyms[x]:
                keywords_and_synonyms[x].append(keywords[x])

        for x in range(len(keywords_and_synonyms)):
            for element in keywords_and_synonyms[x]:
                synonyms[x].extend(GetEntries(element, dic))


        for x in range(len(weights)):
            for y in synonyms[x]:
                result[y] = weights[x]

    return result

def EncodeAsUTF8(text_file, source_encoding):
    """Re-encodes given text file from specified encoding into UTF-8.
       Appends "_utf8" at the end of resulting text file."""

    if len(text_file.split(".")) > 1:
        trgt_name = ".".join(text_file.split(".")[:-1])
        trgt_name += "_utf8." + text_file.split(".")[-1]

    else:
        trgt_name = text_file + "_utf8"

    with codecs.open(text_file, "r", source_encoding) as src:
        with codecs.open(trgt_name, "w", "utf-8") as trgt:
            while True:
                contents = src.read(BLOCKSIZE)
                if not contents:
                    break
                trgt.write(contents)

def ReplaceAll(text, dic):
    """Replaces all occurrences of characters in the text
       according to the rules specified in the dictionary.

       Dictionary syntax: { "<char_to_be_replaced>" : "<replacement>" , ... }"""

    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def ReplaceDiacritics(string):
    """Replaces diacritics in a given UTF-8 string."""

    pol2eng = { "\xc4\x85" : "a" , "\xc4\x84" : "A" ,
                "\xc5\xbc" : "z" , "\xc5\xbb" : "Z" ,
                "\xc5\xba" : "z" , "\xc5\xb9" : "Z" ,
                "\xc5\x82" : "l" , "\xc5\x81" : "L" ,
                "\xc4\x87" : "c" , "\xc4\x86" : "C" ,
                "\xc5\x84" : "n" , "\xc5\x83" : "N" ,
                "\xc4\x99" : "e" , "\xc4\x98" : "E" ,
                "\xc5\x9b" : "s" , "\xc5\x9a" : "S" ,
                "\xc3\xb3" : "o" , "\xc3\x93" : "O" }

    return ReplaceAll(string, pol2eng)

def WeightCounter(text_line, weights):
    weight = 0

    for key in weights:
        if key in text_line:
            weight += weights[key]

    return (weight, text_line)

def GetSentences(text, dic):
    """Returns a list of sentences from a given text."""
    
    ListOfSentences = []
    Sentence = ''
    Shortcuts = []

    for line in dic:
        for word in line.split(';'):
            if re.match('[a-zA-Z0-9_\'\"\-\&\%\$\@\(\)]+\.', word):
                Shortcuts.append(word)
    
    wordList = text.split()
    for word in wordList:
        Sentence = Sentence + ' ' + word
        if re.match('[a-zA-Z0-9_\'\"\-\&\%\$\@\(\)]+[\.\?\!]', word) and not re.match('[0-9]{2}\.',word) and not re.match('[A-Z]\.',word) and word not in Shortcuts:
            ListOfSentences.append(Sentence.strip())
            Sentence = ''

    return ListOfSentences

if __name__ == "__main__":
    if len(argv) == 1:
        print("usage: %s FILENAME" % (argv[0]))

    else:
        text_file = argv[1]
        text = ''

        temp = raw_input("Dawaj pytanie: ")

        with open(text_file, "r") as src:
            for line in src.readlines():
                text = text + ReplaceDiacritics(line) + ' '
            
        with open("odmiany.txt", "r") as dic:
            dic = [ReplaceDiacritics(line) for line in dic.readlines()]

        with open("thesaurus.txt", "r") as dic2:
            dic2 = [ReplaceDiacritics(line) for line in dic2.readlines()]
        
        keyword_weights = ExtractKeywords(temp,dic,dic2)

        results = [WeightCounter(sentence, keyword_weights) for sentence in GetSentences(text,dic)]

        results.sort(reverse = True)

        for result in results:
            if result[0] != 0:
                print("Waga: %d\n%s" % (result[0], result[1]))
