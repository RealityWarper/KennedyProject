#!/usr/bin/python

from __future__ import print_function
from sys import argv
import fun
import re
from google import google_search

if __name__ == "__main__":
    if len(argv) == 1:
        print("usage: {0} FILENAME\n"
              "       {0} -l [number_of_links_to_process]"
              .format(argv[0]))

    else:
        print("Wczytywanie slownika odmian...")
        fun.LoadInflections()

        temp = raw_input("Dawaj pytanie [Kto zabil Kennedy'ego w Dallas?]: ")
        if not temp:
            temp = "Kto zabil Kennedy'ego w Dallas?"
        print("Wydobywanie slow kluczowych z pytania...")
        keyword_weights = fun.ExtractKeywords(temp)

        if(argv[1] == '-l'):
            print("Pobieranie tekstow do analizy z Internetu...")
            try:
                n = int(argv[2])
            except (ValueError, IndexError):
                n = 5
            text = google_search(temp, n)
        else:
            print("Wczytywanie tekstu z pliku...")
            with open(argv[1], "r") as src:
                text = src.read()

        text = fun.ReplaceDiacritics(text)

        print("Obliczanie wag dla poszczegolnych zdan w tekscie...")
        results = [fun.WeightCounter(sentence, keyword_weights) for sentence in fun.GetSentences(text,fun.inflections)]
        results = [result for result in results if result]

        results.sort(reverse = True)

        print("Wyszukiwanie nazwisk w tekscie...")
        names = fun.GetNames(results, text)

        print("Obliczanie wag dla nazwisk na podstawie wagi zdan, w ktorych dane nazwisko wystepuje")
        sums = fun.CountUp(names, results, keyword_weights)
        sums.sort(reverse = True)

        print("Wynik:")
        for el in sums:
            print("%s - %d" % (el[1], el[0]))
        print()

        XYZ = re.search("Kto (.+) (.+) w (.+)\?", fun.ReplaceDiacritics(temp))
        fun.AnswerTime(sums[0][1], XYZ.group(1), XYZ.group(2), XYZ.group(3))
