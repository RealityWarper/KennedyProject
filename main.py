#!/usr/bin/python

from __future__ import print_function
from sys import argv
import fun
import re

if __name__ == "__main__":
    if len(argv) == 1:
        print("usage: %s FILENAME" % (argv[0]))

    else:
        fun.LoadInflections()

        temp = raw_input("Dawaj pytanie [Kto zabil Kennedy'ego w Dallas?]: ")
        if not temp:
            temp = "Kto zabil Kennedy'ego w Dallas?"
        keyword_weights = fun.ExtractKeywords(temp)

        text_file = argv[1]

        with open(text_file, "r") as src:
            text = src.read()

        text = fun.ReplaceDiacritics(text)

        results = [fun.WeightCounter(sentence, keyword_weights) for sentence in fun.GetSentences(text,fun.inflections)]
        results = [result for result in results if result]

        results.sort(reverse = True)

        names = fun.GetNames(text)

        sums = fun.CountUp(names, results, keyword_weights)
        sums.sort(reverse = True)

        for el in sums:
            print("%s - %d" % (el[1], el[0]))
        print()

        XYZ = re.search("Kto (.+) (.+) w (.+)\?", fun.ReplaceDiacritics(temp))
        fun.AnswerTime(sums[0][1], XYZ.group(1), XYZ.group(2), XYZ.group(3))
