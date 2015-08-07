#!/usr/bin/env python2
from __future__ import division
import sys, os, json
from pprint import pprint
from collections import Counter

SHOW_CORRECT_LINES = True

from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatize = lemmatizer.lemmatize

script_path = os.path.dirname(os.path.realpath(__file__))
template_folder = os.path.join(script_path, 'data/html_template')

X = 500

from lib import top_x_words, top5000words
topXwords = top_x_words(X)

# maps words to their lemmatized form. like 'words' to 'word' sohteno toeshntoesnht osnehtoesnhotesnhtoenshotensoht
# so if you look up lemma_cache['words']
lemmatized_form = {}
def get_lemmatized_form(w):
    # return lemmatized_form[w] if w in lemmatized_form else lemmatize(w)
    return w

def top5000index(w):
    lemmatized_w = get_lemmatized_form(w)
    if lemmatized_w in top5000words:
        return top5000words.index(lemmatized_w)
    else:
        return None

# this is for checking if a given word equals another one if both are lemmatized
def are_lemma_equal(w1, w2):
    w1_lemmatized = get_lemmatized_form(w1)
    w2_lemmatized = get_lemmatized_form(w2)
    return w1_lemmatized == w2_lemmatized

# maps words to bool values that tell you if the lemmatized version of the word is in the corpus
lemmatized_word_in_corpus = {}
# this is for cached lookup if the given word (lemmatized) is in the given corpus
def in_(w, corpus):
    if w in lemmatized_word_in_corpus:
        return lemmatized_word_in_corpus[w]
    else:
        lemmatized_w = get_lemmatized_form(w)
        v = lemmatized_w in corpus
        lemmatized_word_in_corpus[w] = v
        return v

def percent(a,b):
    if not b: return '[div by 0]'
    len_a, len_b = len(a), len(b)
    return '{}/{} = {:.0%}'.format(len_a, len_b, len_a/len_b)
    # return '{}/{}'.format(a, b)

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

    out = []

    out.append('<table>')
    out.append('<tr>')
    out.append('<th>' + '</th><th>'.join([
        'Reference', '# in top5000 (cap is {})'.format(X), name1, name2,
        '# wrong words base',
        '# wrong words interpolated',
        '# interesting wrong words base',
        '# wrong interesting words interpolated',
        ]) + '</th>')
    out.append('</tr>')

    worsened = 0
    worsened_words = []
    improved = 0
    improved_words = []
    reference_words = []
    wrong_words_baseline = []
    wrong_words_interpolated = []
    wrong_interesting_words_baseline = []
    wrong_interesting_words_interpolated = []

    for line1, line2 in zip(wer_result1, wer_result2):
        try:

            op, ref, hyp1 = line1.split(' | ');
            _, _, hyp2 = line2.split(' | ');
            hyp1 = hyp1.replace('*', '.')
            hyp2 = hyp2.replace('*', '.')

            tr_class = ''

            if are_lemma_equal(hyp1, ref):
                hyp1_class = 'correct'
                if hyp1 != ref:
                    tr_class += ' lemma'
            else:
                hyp1_class = 'false'
                wrong_words_baseline.append(hyp1)

            if are_lemma_equal(hyp2, ref):
                hyp2_class = 'correct'
                if hyp2 != ref:
                    tr_class += ' lemma'
            else:
                hyp2_class = 'false'
                wrong_words_interpolated.append(hyp2)


            # leave out lines where both results are correct if
            # the flag is set
            if not SHOW_CORRECT_LINES and hyp1_class == 'correct' and hyp2_class == 'correct': continue

            tr_class += ' changed' if hyp1_class != hyp2_class else ''
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

            if in_(ref, corpus):
                tr_class += ' interesting'
                if hyp1_class == 'false':
                    wrong_interesting_words_baseline.append(hyp1)
                if hyp2_class == 'false':
                    wrong_interesting_words_interpolated.append(hyp2)



            prefix = '# ' if hyp1 != hyp2 else '  '
            out.append('<tr class="{}">'.format(tr_class))
            out.append('<td class={}>{}</td>'.format('', ref))
            out.append('<td>{}</td>'.format(top5000index(ref) or '-'))
            out.append('<td class={}>{}</td>'.format(hyp1_class, hyp1))
            out.append('<td class={}>{}</td>'.format(hyp2_class, hyp2))
            out.append('<td>{}</td>'.format(len(wrong_words_baseline)))
            out.append('<td>{}</td>'.format(len(wrong_words_interpolated)))
            out.append('<td>{}</td>'.format(len(wrong_interesting_words_baseline)))
            out.append('<td>{}</td>'.format(len(wrong_interesting_words_interpolated)))
            out.append('</tr>')
        except ValueError: # last line
            pass

    out.append('</table>')

    interesting_words = [w for w in reference_words if w in corpus]

    worsened_words_top = [w for w in worsened_words if not in_(w, corpus)]
    worsened_words_interesting = [w for w in worsened_words if in_(w, corpus)]
    improved_words_top = [w for w in improved_words if not in_(w, corpus)]
    improved_words_interesting = [w for w in improved_words if in_(w, corpus)]

    formatted_worsened_words_top = format_as_bag(worsened_words_top, corpus)
    formatted_worsened_words_not_top = format_as_bag(worsened_words_interesting, corpus)

    formatted_improved_words_top = format_as_bag(improved_words_top, corpus)
    formatted_improved_words_not_top = format_as_bag(improved_words_interesting, corpus)


    out.append('<br/><p>Wrong words baseline: {}</br> Wrong words interpolated: {}</p>'.format(
        percent(wrong_words_baseline, reference_words),
        percent(wrong_words_interpolated, reference_words)
    ))

    out.append('<br/><p>Wrong interesting words baseline: {}</br> Wrong interesting words interpolated: {}</p>'.format(
        percent(wrong_interesting_words_baseline, interesting_words),
        percent(wrong_interesting_words_interpolated, interesting_words)
    ))


    out.append('<br/><p>Worsened: {}; Improved: {}</p>'.format(
        worsened, improved))
    out.append('<p>Overall words: {}; Interesting words: {}</p>'.format(len(reference_words), len(interesting_words)))

    explanation = "Interesting words: in (slides corpus - top {})".format(X)

    worsenedWordsRatio = percent(worsened_words, reference_words)
    worsenedWordsInterestingRatio = percent(worsened_words_interesting, worsened_words)
    interestingWordsWorsenedRatio = percent(worsened_words_interesting, interesting_words)
    improvedWordsRatio = percent(improved_words, reference_words),
    improvedWordsInterestingRatio = percent(improved_words_interesting, improved_words)
    interestingWordsImprovedRatio = percent(improved_words_interesting, interesting_words)

    out.append('<br/><p>{}</p>'.format(explanation))
    out.append('''
            <br/>
            <p>
                <b>Worsened Words ({worsenedWordsRatio})
                </b> ({worsenedWordsInterestingRatio} are interesting; 
                We worsened {interestingWordsWorsenedRatio} of the overall interesting words).
            </p>

            <u>Non-interesting words</u></br>
            <p>{formatted_worsened_words_top}</p>
            <br/>
            <u>Interesting words</u></br>
            <p>{formatted_worsened_words_not_top}</p>
            <br/>
            <p>
                <b>Improved Words ({improvedWordsRatio})</b> 
                ({improvedWordsInterestingRatio} are interesting; 
                We improved {interestingWordsImprovedRatio} of the overall interesting words).
            </p>
            <u>Non-interesting words</u></br>
            <p>{formatted_improved_words_top}</p>
            <br/>
            <u>Interesting words</u></br>
            <p>{formatted_improved_words_not_top}</p>
        '''.format(
        worsenedWordsRatio=worsenedWordsRatio,
        worsenedWordsInterestingRatio=worsenedWordsInterestingRatio,
        interestingWordsWorsenedRatio=interestingWordsWorsenedRatio,

        formatted_worsened_words_top=formatted_worsened_words_top,
        formatted_worsened_words_not_top=formatted_worsened_words_not_top,

        improvedWordsRatio=improvedWordsRatio,
        improvedWordsInterestingRatio=improvedWordsInterestingRatio,
        interestingWordsImprovedRatio=interestingWordsImprovedRatio,

        formatted_improved_words_top=formatted_improved_words_top,
        formatted_improved_words_not_top=formatted_improved_words_not_top
        )
    )

    out.append('<br/><p>{}: {}</p>'.format(name1, summary1))
    out.append('<p>{}: {}</p>'.format(name2, summary2))

    print(template.format(css, '\n'.join(out)))

    stats = dict(
        words=len(reference_words),
        interesting_words=len(interesting_words),
        worsenedWordsRatio=worsenedWordsRatio,
        worsenedWordsInterestingRatio=worsenedWordsInterestingRatio,
        interestingWordsWorsenedRatio=interestingWordsWorsenedRatio,
        improvedWordsRatio=improvedWordsRatio,
        improvedWordsInterestingRatio=improvedWordsInterestingRatio,
        interestingWordsImprovedRatio=interestingWordsImprovedRatio,
    )

    open('results.json', 'w').write(json.dumps(stats, sort_keys=True, indent=2, separators=(', ', ': ')))

def main_():
    args = sys.argv[1:]
    wer_result1 = open(args[0]).read().split('\n')[:-1]
    wer_result2 = open(args[1]).read().split('\n')[:-1]

    name1 = args[2] # for table headers
    name2 = args[3] # ...
    corpus = open(args[4]).read().split()[:-1]
    corpus_without_top_words = \
        [w for w in corpus if not get_lemmatized_form(w) in topXwords]
    template = open(os.path.join(template_folder, 'template.html')).read()
    css = open(os.path.join(template_folder, 'style.css')).read()
    compare(wer_result1, wer_result2, name1, name2, template, css,corpus_without_top_words)

main_()



