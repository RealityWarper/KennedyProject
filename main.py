#!/usr/bin/python

from __future__ import print_function
from sys import argv

def ReplaceAll(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def WeightCounter(text_line, weights):
    weight = 0

    for key in weights:
        if key in text_line:
            weight += weights[key]

    return (weight, text_line)


if __name__ == "__main__":
    if len(argv) == 1:
        print("usage: %s FILENAME" % (argv[0]))

    else:
        keyword_weights = { "Kennedy" : 30 , "zabi" : 60 , "Dallas" : 20 , "mord" : 60 }

        # ponizsze przelozenia dzialaja, ale tylko przy pliku kodowanym w utf-8
        # np. odmiany.txt mamy juz kodowane czyms innym

        pol2eng = { "\xc4\x85" : "a" , "\xc4\x84" : "A" ,
                    "\xc5\xbc" : "z" , "\xc5\xbb" : "Z" ,
                    "\xc5\xba" : "z" , "\xc5\xb9" : "Z" ,
                    "\xc5\x82" : "l" , "\xc5\x81" : "L" ,
                    "\xc4\x87" : "c" , "\xc4\x86" : "C" ,
                    "\xc5\x84" : "n" , "\xc5\x83" : "N" ,
                    "\xc4\x99" : "e" , "\xc4\x98" : "E" ,
                    "\xc5\x9b" : "s" , "\xc5\x9a" : "S" ,
                    "\xc3\xb3" : "o" , "\xc3\x93" : "O" }

        text_file = argv[1]

        with open(text_file, "r") as src:
            lines = src.readlines()

        lines = [ReplaceAll(line, pol2eng) for line in lines]

        results = [WeightCounter(line, keyword_weights) for line in lines]

        results.sort(reverse = True)

        for result in results:
            if result[0] != 0:
                print("Waga: %d\n%s" % (result[0], result[1]))
