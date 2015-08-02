#!/usr/bin/env python3
import sys
import json
from pprint import pprint

# main()

def main():
    # load a result from `wordpositions
    args = sys.argv[1:]
    word_count_file = args[0]
    word_counts = json.load(open(word_count_file))
    # pprint(word_counts)

    word_results = []
    found_overall = sum(len(w['positions']) for w in word_counts)
    actual_overall = sum(w['freq'] for w in word_counts)
    # for word in word_counts:
    #     reference_freq = word['freq']
    #     found_freq = len(word['positions'])
    #     w = word['word']
    #     word_results.append([w, found_freq/reference_freq])

    print('found {}/{} keywords = {:4.2f}% KWER'.format(found_overall, actual_overall, 100*(1-(found_overall/actual_overall))))

main()
