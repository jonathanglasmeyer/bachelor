#!/usr/bin/env python3
from pprint import pprint
import json
import sys
from collections import Counter

def main():
    args = sys.argv[1:]

    # an output from filter.py
    word_count_file = args[0]

    word_freqs = Counter(json.load(open(word_count_file)))
    word_freqs_common = word_freqs.most_common()
    print('\n'.join(list(reversed([': '.join([a,str(b)]) for a,b in word_freqs_common]))))

main()
