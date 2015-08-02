#!/usr/bin/env python3
import sys
from collections import Counter
from pprint import pprint

def main():
    args = sys.argv[1:]
    # arg 1: corpus file

    corpus_file = args[0]
    words = open(corpus_file).read().split()
    counter = Counter(words)
    n = 60

    # n least common elements
    counts = counter.most_common()[:-n-1:-1]

    pprint([(w.lower(), n) for w,n in counts])

main()
