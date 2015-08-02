#!/usr/bin/env python3
import sys
from pprint import pprint
from collections import Counter

SHOW_CORRECT_LINES = True

# from nltk.stem.wordnet import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# lemmatize = lemmatizer.lemmatize

FILTER_BY_CORPUS = True
if FILTER_BY_CORPUS:
    X = 500
else: 
    X = 800

top5000words = open('/home/jwerner/uni/bachelor/bin/top5000.txt').read().split('\n')[:-1]
topXwords=top5000words[:X]


def in_(w, corpus):
    # TODO: get nltk installed again
    # return lemmatize(w) in corpus
    return w in corpus or w + 's' in corpus

def percent(a,b):
    return '{}/{} = {:.0%}'.format(a, b, a/b)
    # return '{}/{}'.format(a, b)

def format_word(word, count, corpus):
    corpus_ = corpus if FILTER_BY_CORPUS else topXwords
    # if we filter by corpus, the class topword should be applied
    # if the word isn't in the corpus
    # if we filter by topword it is the other way round
    bool = not FILTER_BY_CORPUS


    return '<span class="topword">({}, {})</span>'.format(word, count) if in_(word, corpus_) == bool else '<span>({}, {})</span>'.format(word, count)

def format_as_bag(words, corpus):
    # print(''.format(Counter(words).most_common())
    formatted_words = [format_word(w, count, corpus) for w, count in Counter(words).most_common()]
    return ' '.join(formatted_words)

def filter_out_INS(result):
    return [l for l in result
        if '|' in l and l.split(' | ')[0] != 'INS']

def compare(wer_result1, wer_result2, name1, name2, template, corpus_without_top_words):
    if FILTER_BY_CORPUS:
        corpus = corpus_without_top_words
    else:
        corpus = topXwords
    # print ('HYP1: {}'.format(fname1))
    # print ('HYP2: {}'.format(fname2))

    summary1 = wer_result1[-1]
    summary2 = wer_result2[-1]
    wer_result1 = filter_out_INS(wer_result1)[1:]
    wer_result2 = filter_out_INS(wer_result2)[1:]

    out = []

    out.append('<table>')
    out.append('<tr>')
    out.append('<th>' + '</th><th>'.join(['Reference', name1, name2]) + '</th>')
    out.append('</tr>')

    worsened = 0
    worsened_words = []
    improved = 0
    improved_words = []
    reference_words = []

    for line1, line2 in zip(wer_result1, wer_result2):
        try:
            op, ref, hyp1 = line1.split(' | ');
            _, _, hyp2 = line2.split(' | ');
            hyp1 = hyp1.replace('*', '.')
            hyp2 = hyp2.replace('*', '.')
            hyp1_class = 'correct' if hyp1 == ref else 'false'
            hyp2_class = 'correct' if hyp2 == ref else 'false'

            # leave out lines where both results are correct if
            # the flag is set
            if not SHOW_CORRECT_LINES and hyp1_class == 'correct' and hyp2_class == 'correct': continue

            tr_class = 'interesting' if hyp1_class != hyp2_class else ''
            if hyp1_class == 'correct' and hyp2_class == 'false':
                tr_class += ' worsened'
                worsened += 1
                worsened_words.append(hyp1)
            elif hyp1_class == 'false' and hyp2_class == 'correct':
                tr_class += ' improved'
                improved += 1
                improved_words.append(hyp2)
            ref = ref.replace('*', '.')
            reference_words.append(ref)
            prefix = '# ' if hyp1 != hyp2 else '  '
            out.append('<tr class="{}">'.format(tr_class))
            out.append('<td class={}>{}</td>'.format('', ref))
            out.append('<td class={}>{}</td>'.format(hyp1_class, hyp1))
            out.append('<td class={}>{}</td>'.format(hyp2_class, hyp2))
            out.append('</tr>')
        except ValueError: # last line
            pass

    out.append('</table>')
    # this has nothing to do with good code
    # anyway. :)

    # TODO: percentage should be calc'd differently
    # -> in relation to all interesting words.

    if FILTER_BY_CORPUS:
        interesting_words = [w for w in reference_words 
                if w in corpus]

        worsened_words_top = [w for w in worsened_words 
                if not in_(w, corpus)]
        worsened_words_interesting = [w for w in worsened_words 
                if in_(w, corpus)]
        improved_words_top = [w for w in improved_words 
                if not in_(w, corpus)]
        improved_words_interesting = [w for w in improved_words 
                if in_(w, corpus)]
    else:
        interesting_words = [w for w in reference_words 
                if w not in corpus]
        worsened_words_top = [w for w in worsened_words 
                if in_(w, corpus)]
        worsened_words_interesting = [w for w in worsened_words 
                if not in_(w, corpus)]
        improved_words_top = [w for w in improved_words 
                if in_(w, corpus)]
        improved_words_interesting = [w for w in improved_words 
                if not in_(w, corpus)]

    # worsened_words_sorted = \
    #     worsened_words_top + worsened_words_interesting
    # improved_words_sorted = \
    #     improved_words_top + improved_words_interesting

    formatted_worsened_words_top = format_as_bag(worsened_words_top, corpus)
    formatted_worsened_words_not_top = format_as_bag(worsened_words_interesting, corpus)

    formatted_improved_words_top = format_as_bag(improved_words_top, corpus)
    formatted_improved_words_not_top = format_as_bag(improved_words_interesting, corpus)

    out.append('<br/><p>Worsened: {}; Improved: {}</p>'.format(
        worsened, improved))
    out.append('<p>Overall words: {}; Interesting words: {}</p>'.format(len(reference_words), len(interesting_words)))

    explanation = 'Interesting words: not in topX of the most common words. X = {}'.format(X) if not FILTER_BY_CORPUS else 'Interesting words: in corpus'
    out.append('<br/><p>{}</p>'.format(explanation))
    out.append('''
            <br/>
            <p>
                <b>Worsened Words ({})</b> ({} are interesting; {} interesting words worsened):
            </p>

            <p>{}</p>
            <br/> 
            <p>{}</p>
            <br/> 
            <p>
                <b>Improved Words ({})</b> ({} are interesting; {} interesting words improved): 
            </p>
            <p>{}</p>
            <br/> 
            <p>{}</p>
        '''.format(
        percent(len(worsened_words), len(reference_words)),
        percent(len(worsened_words_interesting), len(worsened_words)),
        percent(len(worsened_words_interesting), len(interesting_words)),
        formatted_worsened_words_top,
        formatted_worsened_words_not_top,

        percent(len(improved_words), len(reference_words)),
        percent(len(improved_words_interesting), len(improved_words)),
        percent(len(improved_words_interesting), len(interesting_words)),
        formatted_improved_words_top,
        formatted_improved_words_not_top
        )
    )

    out.append('<br/><p>{}: {}</p>'.format(name1, summary1))
    out.append('<p>{}: {}</p>'.format(name2, summary2))
    print(template.format('\n'.join(out)))

def main_():
    args = sys.argv[1:]
    wer_result1 = open(args[0]).read().split('\n')[:-1]
    wer_result2 = open(args[1]).read().split('\n')[:-1]
    name1 = args[2] # for table headers
    name2 = args[3] # ...
    corpus = open(args[4]).read().split()[:-1]
    corpus_without_top_words = \
        [w for w in corpus if w not in topXwords]
    template = open('/home/jwerner/uni/bachelor/bin/compare-wer/template.html').read()
    compare(wer_result1, wer_result2, name1, name2, template, corpus_without_top_words)

main_()
