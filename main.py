#!/usr/bin/python

from __future__ import print_function
from sys import argv
import fun

# WAZNE - systemy unixowe i windows maja rozne zakonczenia linii - dlatego juz dwa commity
# mowia ze wszystko sie zmienilo, mimo ze wyglada tak samo. Poza tym jak otwieram
# windowsowskie pliki na linuksie to musze to zmieniac zeby dzialalo - najlepiej
# poszukac w edytorze opcji typu <End Of Line conversion> i przerzucic na Unix,
# windows sobie poradzi.
#
#
# Dobra, tutaj wrzuce komentarze odnosnie tych konkretnych zmian ktore wprowadzilem.
# Slowniki raz ladowane dla wszystkich sa okej, zmienilem je po prostu w globalne.
# Przerzucilem funkcje do modulu fun.py zeby bylo widac co sie dzieje.
# zmienilem wczytywanie tekstu, ReplaceDiacritics intencjonalnie moze przyjac string.
# Domyslne pytanie (to i tak testowe).
# Wyczyscilem GetSentences troche - rozumiem ze te dlugie grupy znakow w [] to dowolny znak?
# Spacji i tak nie bedzie, wiec pominalem.
#
# Dwukrotnie niezaleznie pojawil sie pomysl zeby zmienic strukture wykorzystywanego
# slownika odmian na rdzenie + koncowki odmian: pewnie drzewo liter dla rdzeni i slowniki
# koncowek jako liscie, jeszcze spojrze co najlepiej tu zadziala, poza tym trzeba
# obejrzec ten plWordNet Vetulaniego, lepiej przed zmiana slownikow zeby nie dublowac wysilkow.
# Usunie to tez zaprzeczenia ze starego slownika.

if __name__ == "__main__":
    if len(argv) == 1:
        print("usage: %s FILENAME" % (argv[0]))

    else:
        fun.LoadDictionaries()

        temp = raw_input("Dawaj pytanie [Kto zabil Kennedy'ego w Dallas?]: ")
        if not temp:
            temp = "Kto zabil Kennedy'ego w Dallas?"
        keyword_weights = fun.ExtractKeywords(temp)

        text_file = argv[1]

        with open(text_file, "r") as src:
            text = src.read()

        text = fun.ReplaceDiacritics(text)

        results = [fun.WeightCounter(sentence, keyword_weights) for sentence in fun.GetSentences(text,fun.inflections)]

        results.sort(reverse = True)

        for result in results:
            if result[0] != 0:
                print("Waga: %d\n%s" % (result[0], result[1]))
