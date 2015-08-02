#!/usr/bin/env python2
from __future__ import division, print_function, unicode_literals
import sys, json, os
from itertools import groupby
from contractions import contractions as contractions_

from pprint import pprint
from collections import Counter

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatize = lemmatizer.lemmatize

data_resources_folder = '/home/jwerner/uni/bachelor/bin'

def calculate_keyword_wers(wer_lines):
    # print('-'*60)
    groups = []
    keyfunc = lambda l: lemmatize(l[1].lower())
    data = sorted(wer_lines, key=keyfunc)
    keyword_to_wer_map = {}
    overall_count = 0
    overall_recognized = 0
    for k, g in groupby(data, keyfunc):
        group = list(g)
        count_for_word = len(group)
        overall_count += count_for_word

        count_recognized_correctly = len([l for l in group if l[0] == 'OK'])
        overall_recognized += count_recognized_correctly
        wcr = count_recognized_correctly / count_for_word
        keyword_to_wer_map[k] = {
                'count': count_for_word,
                'recognized': count_recognized_correctly,
                'wcr': wcr
                }

    sorted_ = sorted(keyword_to_wer_map.items(), key=lambda kw: kw[1]['count'], reverse=True)
    for keyword, values in sorted_:
        print('{} ({}/{})'.format(keyword, values['recognized'], values['count']))
    print('{}/{} keywords recognized => {}% WER.'.format(
        overall_recognized, overall_count, 100-(100*overall_recognized/overall_count)))

keywords_file = os.path.join(data_resources_folder, 'keywords.txt')
top5000_file = os.path.join(data_resources_folder, 'top5000.txt')

keywords = set([w.lower() for w in open(keywords_file).read().split()])
top5000words = open('/home/jwerner/uni/bachelor/bin/top5000.txt').read().split('\n')[:-1]
top5000words=top5000words[:500]

def keyword_wer(frequent_keywords, wer_file):
    wer_lines = unicode(open(wer_file).read(), 'utf-8').split('\n')[1:-6]
    wer_data = [line.split('\t') for line in wer_lines]
    wer_data_keyword_filtered = \
        [(op, ref, hyp) for op, ref, hyp in wer_data if lemmatize(ref.lower()) in frequent_keywords]

    return wer_data_keyword_filtered


def frequent_keywords(f):
    """
    words that are in psychology keywords and not in
    top1000 most frequent words
    """
    hyp = [w.lower() for w in open(f).read().split()]
    hyp = [unicode(w, 'utf-8') for w in hyp]

    hyp_tags = pos_tag(hyp)
    hyp_nouns = [w for w,pos in pos_tag(hyp) if pos in ['NNP', 'NN', '-NONE-', 'NNS']]
    lemmatized_nouns = map(lemmatize, hyp_nouns)
    counter = Counter(lemmatized_nouns)
    counts = counter.most_common()

    frequent_keywords = []
    for w,n in [(w.lower(), n) for w,n in counts]:
        if w in keywords and w not in top5000words[:1000]:
            frequent_keywords.append(w)
            # print('{} ({})'.format(w, n))


    return frequent_keywords


def unfrequent_nouns(f):
    """
    - take a recognition result (raw text) and filter out the top x most common words. (plus variants of those like plurals) (x = 500 right now).
    - remove short words (<3 chars) and words with "'" in them
    - export those words and their counts into json (stdout)
    """

    top5000words_with_variants = set(top5000words)

    for w in top5000words:
        if len(w) >= 3:
            top5000words_with_variants |= {w + 's'}
            top5000words_with_variants |= {w + 'ing'}
            top5000words_with_variants |= {w + 'ting'}
            top5000words_with_variants |= {w + 'ed'}
            top5000words_with_variants |= {w + 'ped'}
            top5000words_with_variants |= {w + 'd'}
            top5000words_with_variants |= {w + '\'s'}
            top5000words_with_variants |= {w + '\'ll'}

    contractions = set(contractions_.keys())
    top5000words_with_variants |= contractions

    hyp = [unicode(w.lower(), 'utf-8') for w in open(f).read().split()]
    # hyp_nouns = (w for w,pos in pos_tag(hyp) if 
        # pos in ['NNP', 'NN', '-NONE-', 'NNS'])
    hyp_lemmatized = (lemmatize(w) for w in hyp)

    # remove short words and words with '
    hyp_lemmatized = \
        (w for w in hyp_lemmatized if 
            len(w) >= 3 and not "'" in w)

    hyp_special = (w for w in hyp_lemmatized if w not in top5000words)
    bag = Counter(hyp_special)

    json_ = json.dumps(
        {word: count for word, count in bag.most_common()}, indent=2)
    print(json_)

def frequent(f, wer_file):
    frequent_keywords_ = frequent_keywords(f)
    wer_lines = keyword_wer(frequent_keywords_, wer_file)
    calculate_keyword_wers(wer_lines)

def main():
    args = sys.argv[1:]

    # a recognition results file
    f = args[0]

    # wer_file = args[1]

    # frequent(f, wer_file)
    unfrequent_nouns(f)
        # print(w)

main()
