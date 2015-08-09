#!/usr/bin/env python3
import sys, os
from subprocess import call
from os.path import join, isdir

script_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.abspath(join(script_path, os.pardir))
results_path = join(project_path, 'results')
viz_data_path = join(project_path, 'viz/public/data')

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print('hotword-analyze.py testcase_name')
        sys.exit()

    testcase_name = args[0]

    testcase_dir = join(results_path, testcase_name)
    assert isdir(testcase_dir)

    def call_(cmd):
        print(cmd)
        return call(cmd, cwd=testcase_dir, shell=True)


    # call_('filter.py reference.corpus.txt > reference_wordcounts.json')
    # for mode in ['baseline', 'interpolated']:
        # call_('wordpositions reference_wordcounts.json sphinx_word_times_{mode}.txt > cloud_{mode}.json'.format(mode=mode))
        # call_('cluster.py cloud_{mode}.json'.format(mode=mode))
        # call_('cp cloud_{mode}.json {folder}/{name}_{mode}.json'.format(mode=mode, name=testcase_name, folder=viz_data_path))
        # call_('cp resources/audio.wav {folder}/{name}.wav'.format(mode=mode, name=testcase_name, folder=viz_data_path))

        # call_('wer.py reference.corpus.txt sphinx_result_{mode}.txt > wer_{mode}.txt'.format(mode=mode))

    call_('compare-wer.py wer_baseline.txt wer_interpolated.txt baseline interpolated slides.corpus.txt > wer_comparison.html')

main()

