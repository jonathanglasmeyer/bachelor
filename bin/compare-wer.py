#!/usr/bin/env python2
from __future__ import division
import sys, os, json
from pprint import pprint
from collections import Counter

SHOW_CORRECT_LINES = True

# Show all words in a table
DETAILED = True

PRINT_HTML = True

def log(*text):
    if not PRINT_HTML:
        print(text)

def print_paragraph(text):
    if PRINT_HTML:
        print('<p>{}</p>'.format(text))

def print_key_value(key, value):
    if PRINT_HTML:
        print('<p><b>{}</b>:</p>'.format(key))
        print('<p>{}</p>'.format(value))

from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
_lemmatize = lemmatizer.lemmatize

X=500

script_path = os.path.dirname(os.path.realpath(__file__))
template_folder = os.path.join(script_path, 'data/html_template')

from lib import top_x_words, top5000words
topXwords = top_x_words(X)

# memoized lemma lookup
lemmatized_form = {}
def lemmatize(w):
    if w in lemmatized_form:
        return lemmatized_form[w]
    else:
        lemma = _lemmatize(w)
        lemmatized_form[w] = lemma
        return lemma

def top5000index(w):
    lemmatized_w = lemmatize(w)
    if lemmatized_w in top5000words:
        return top5000words.index(lemmatized_w)
    else:
        return None

# this is for checking if a given word equals another one if both are lemmatized

def are_lemma_equal(w1, w2):
    w1_lemmatized = lemmatize(w1)
    w2_lemmatized = lemmatize(w2)
    return w1_lemmatized == w2_lemmatized

# maps words to bool values that tell you if the lemmatized version of the word is in the corpus
lemmatized_word_in_corpus = {}
# this is for cached lookup if the given word (lemmatized) is in the given corpus
def in_(w, corpus):
    if w in lemmatized_word_in_corpus:
        return lemmatized_word_in_corpus[w]
    else:
        lemmatized_w = lemmatize(w)
        v = lemmatized_w in corpus
        lemmatized_word_in_corpus[w] = v
        return v

def percent(a,b, inverse=False):
    if not b: return '[div by 0]'
    len_a, len_b = len(a), len(b)
    if inverse:
        return '1 - {}/{} = {:.0%}'.format(len_a, len_b, 1 - (len_a/len_b))
    else:
        return '{}/{} = {:.0%}'.format(len_a, len_b, len_a/len_b)

def format_word(word, count, corpus):
    return '<span>({}, {})</span>'.format(word, count)

def format_as_bag(words, corpus):
    formatted_words = [format_word(w, count, corpus) for w, count in Counter(words).most_common()]
    return ' '.join(formatted_words)

def filter_out_INS(result):
    return [l for l in result
        if '|' in l and l.split(' | ')[0] != 'INS']

def compare(wer_result1, wer_result2, name1, name2, template, css, corpus_without_top_words):
    corpus = corpus_without_top_words

    summary1 = wer_result1[-1]
    summary2 = wer_result2[-1]
    wer_result1 = filter_out_INS(wer_result1)[1:]
    wer_result2 = filter_out_INS(wer_result2)[1:]
    # print(wer_result1)

    out = []

    if DETAILED:
        out.append('<table>')
        out.append('<tr>')
        out.append('<th>' + '</th><th>'.join([
            'Reference', #'# in top5000 (cap is {})'.format(X), 
            name1, name2,
            '# wrong words A',
            '# wrong words B',
            '# wrong keywords A',
            '# wrong interesting words B',
            ]) + '</th>')
        out.append('</tr>')

    worsened_words = []
    improved_words = []
    reference_words = []
    wrong_words_A = []
    wrong_words_B = []
    wrong_keywords_A = []
    wrong_keywords_B = []

    for line1, line2 in zip(wer_result1, wer_result2):
        try:

            op, ref_original, hyp1_original = line1.split(' | ');
            _, _, hyp2_original = line2.split(' | ');

            hyp1_original = hyp1_original.replace('*', '.')
            hyp2_original = hyp2_original.replace('*', '.')
            ref_original = ref_original.replace('*', '.')

            ref = lemmatize(ref_original)
            hyp1 = lemmatize(hyp1_original)
            hyp2 = lemmatize(hyp2_original)

            reference_words.append(ref)

            tr_class = ''

            if hyp1 == ref:
                hyp1_class = 'correct'
                if hyp1_original != ref_original:
                    tr_class += ' lemma'
            else:
                hyp1_class = 'false'
                wrong_words_A.append(ref)

            if hyp2 == ref:
                hyp2_class = 'correct'
                if hyp2_original != ref_original:
                    tr_class += ' lemma'
            else:
                hyp2_class = 'false'
                wrong_words_B.append(ref)


            # leave out lines where both results are correct if
            # the flag is set
            if not SHOW_CORRECT_LINES and hyp1_class == 'correct' and hyp2_class == 'correct': continue

            tr_class += ' changed' if hyp1_class != hyp2_class else ''
            if hyp1_class == 'correct' and hyp2_class == 'false':
                tr_class += ' worsened'
                worsened_words.append(ref)
            elif hyp1_class == 'false' and hyp2_class == 'correct':
                tr_class += ' improved'
                improved_words.append(ref)

            if in_(ref, corpus):
                tr_class += ' interesting'
                if hyp1_class == 'false':
                    wrong_keywords_A.append(ref)
                if hyp2_class == 'false':
                    wrong_keywords_B.append(ref)



            prefix = '# ' if hyp1 != hyp2 else '  '
            if DETAILED:
                out.append('<tr class="{}">'.format(tr_class))
                out.append('<td class={}>{}</td>'.format('', ref_original))
                out.append('<td class={}>{}</td>'.format(hyp1_class, hyp1_original))
                out.append('<td class={}>{}</td>'.format(hyp2_class, hyp2_original))
                out.append('</tr>')
        except ValueError: # last line
            pass

    out.append('</table>')

    lemmatized_reference_words = map(lemmatize, reference_words)
    keywords = [w for w in lemmatized_reference_words if w in corpus]

    log('keywords: ', keywords);
    log('corpus: ', corpus);
    log('lemmatized_reference_words: ', lemmatized_reference_words);
    print_key_value('keywords', keywords)

    worsened_words_normal = [w for w in worsened_words if not in_(w, corpus)]
    worsened_keywords = [w for w in worsened_words if in_(w, corpus)]
    improved_words_normal = [w for w in improved_words if not in_(w, corpus)]
    improved_keywords = [w for w in improved_words if in_(w, corpus)]

    W = len(reference_words)

    WDR_A = percent(wrong_words_A, reference_words, inverse=True)
    WDR_B = percent(wrong_words_B, reference_words, inverse=True)
    W_worse = percent(worsened_words, reference_words)
    W_improved = percent(improved_words, reference_words)
    W_worse_K = percent(worsened_keywords, worsened_words)
    W_improved_K = percent(improved_keywords, improved_words)

    KW = len(keywords)

    KWDR_A = percent(wrong_keywords_A, keywords, inverse=True)
    log('KWDR_A', KWDR_A)
    KWDR_B = percent(wrong_keywords_B, keywords, inverse=True)
    KW_worse = percent(worsened_keywords, keywords)
    KW_improved = percent(improved_keywords, keywords)

    stats = dict(
        W=W,
        KW=KW,

        WDR_A=WDR_A,
        WDR_B=WDR_B,
        W_worse=W_worse,
        W_improved=W_improved,

        KWDR_A=KWDR_A,
        KWDR_B=KWDR_B,
        KW_worse=KW_worse,
        KW_improved=KW_improved,

        W_worse_K=W_worse_K,
        W_improved_K=W_improved_K
    )

    out.append('<pre><code>{}</code></pre>'.format(
        json.dumps(stats, sort_keys=True, indent=2, separators=(', ', ': '))))

    def print_bag(bag, caption):
        out.append('''
            <br/>
            <b>{caption}</b><br/>
            {bag}
            <br/>
        '''.format(caption=caption, bag=bag))

    bag_IW_worse = format_as_bag(worsened_keywords, corpus)
    bag_W_improved = format_as_bag(improved_words_normal, corpus)
    bag_IW_improved = format_as_bag(improved_keywords, corpus)
    bag_W_worse = format_as_bag(worsened_words_normal, corpus)
    bags = [
        (bag_W_improved, 'Normal words improved'),
        (bag_IW_improved, 'KW improved'),
        (bag_W_worse, 'Normal words worse'),
        (bag_IW_worse, 'KW worse')
    ]

    for bag, caption in bags:
        print_bag(bag, caption)


    out.append('<br/><p>{}: {}</p>'.format(name1, summary1))
    out.append('<p>{}: {}</p>'.format(name2, summary2))
    out.append('<p>{}: {}</p>'.format('X', X))

    if PRINT_HTML:
        print(template.format('Analyze WER/IWER', css, '\n'.join(out)))

    open('results.json', 'w').write(json.dumps(stats, sort_keys=True, indent=2, separators=(', ', ': ')))

def main_():
    args = sys.argv[1:]
    wer_result1 = open(args[0]).read().split('\n')[:-1]
    wer_result2 = open(args[1]).read().split('\n')[:-1]

    name1 = args[2] # for table headers
    name2 = args[3] # ...
    # corpus = open(args[4]).read().split()[:-1]
    corpus = map(lemmatize, open(args[4]).read().split())
    corpus_without_top_words = \
        [w for w in corpus if not lemmatize(w) in topXwords]

    print_key_value('Corpus', corpus)
    print_key_value('Lemmatized corpus without topXwords', corpus_without_top_words)
    
    template = open(os.path.join(template_folder, 'template.html')).read()
    css = open(os.path.join(template_folder, 'style.css')).read()
    compare(wer_result1, wer_result2, name1, name2, template, css,corpus_without_top_words)

main_()



