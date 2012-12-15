import codecs
import re

BLOCKSIZE = 1048576 # 1 MB text buffer
synonyms, inflections = {}, {} # global dictionaries

def Unique(seq):
    """Returns a list of unique elements generated from a given object
       without changing their order."""
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            yield item

def GetEntries(word, dic):
    """Combs a dictionary for lines containing specified word.
       Returns a list of unique semicolon separated entries from those lines."""

    entries = [line.rstrip("\n\r") for line in dic if re.search(";%s;" % (word), line)]

    entries = [word for line in entries for word in line.split(";") if word]

    entries[:] = Unique(entries)

    if not entries:
        entries = [word]

    return entries

def ExtractKeywords(question):
    """Returns a list of X, Y and Z synonyms and their inflections
       from a given question string, expects "Kto X Y w Z?" format."""

    XYZ = [ [] , [] , [] ]
    weights = [ 60, 30, 20 ]

    match = re.search("Kto (.+) (.+) w (.+)\?", ReplaceDiacritics(question))
    result = dict()

    if match:
        keywords = [GetEntries(word, inflections)[0] for word in match.group(1,2,3)]
        keywords_and_synonyms = [GetEntries(word, synonyms) for word in keywords]

        for x in range(len(keywords_and_synonyms)):
            if not keywords_and_synonyms[x]:
                keywords_and_synonyms[x].append(keywords[x])

        for x in range(len(keywords_and_synonyms)):
            for element in keywords_and_synonyms[x]:
               XYZ[x].extend(GetEntries(element, inflections))


        for x in range(len(weights)):
            for y in XYZ[x]:
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
    # liczy slowo pare razy jak powtarza sie rdzen
    # nowy slownik to poprawi
    weight = 0

    for key in weights:
        if key in text_line:
            weight += weights[key]

    return (weight, text_line)

def GetSentences(text, dic):
    """Returns a list of sentences from a given text."""

    ListOfSentences, Shortcuts, Sentence = [], [], ''

    for line in dic:
        for word in line.split(';'):
            # ewentualnie
            # if "." in word:
            if re.match(".+\.$", word):
                Shortcuts.append(word)

    wordList = text.split()
    for word in wordList:
        Sentence += ' ' + word
        if re.match('.+[.?!]', word) and not re.match('[0-9]{2}\.',word) and not re.match('[A-Z]\.',word) and word not in Shortcuts:
            ListOfSentences.append(Sentence.strip())
            Sentence = ''

    return ListOfSentences

def LoadDictionaries():
    global synonyms
    global inflections

    with open("odmiany.txt", "r") as src:
        inflections = [ReplaceDiacritics(line) for line in src.readlines()]

    with open("thesaurus.txt", "r") as src:
        synonyms = [ReplaceDiacritics(line) for line in src.readlines()]
