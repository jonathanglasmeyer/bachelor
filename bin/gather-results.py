#!/usr/bin/env python2
from __future__ import division
from json2html import *
from tabulate import tabulate
import sys, os, json
from pprint import pprint
from os.path import join, isfile

script_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.abspath(join(script_path, os.pardir))
results_path = join(project_path, 'results')

def percent(a,b):
    if not b: return '[div by 0]'
    # return '{}/{} = {:.0%}'.format(a, b, a/b)
    return '{:.0%}'.format(a/b)

def main():
    subdirs = os.listdir(results_path)
    results = []
    for resultDir in subdirs:
        resultFile = join(resultDir, 'results.json')
        resultsExist = isfile(resultFile)
        if resultsExist:
            result = json.load(open(resultFile))
            result['name'] = resultDir
            results.append(result)

    print(json.dumps(results, sort_keys=True, indent=2, separators=(', ', ': ')))

    # table = []
    # for result in results:
    #     table.append([
    #         result['name'],
    #         result['words'],
    #         percent(result['wrong_words_baseline'], result['words']),
    #         percent(result['wrong_words_interpolated'], result['words']),
    #         percent(result['wrong_words_baseline'], result['words']),
    #         percent(result['wrong_words_interpolated'], result['words'])

    #     ])

    # print(tabulate(table, headers=[
    #     'Name',
    #     'Words',
    #     'Wrong words baseline',
    #     'Wrong words interpolated',
    #     'Interesting Wrong Words Baseline',
    #     'WrongI 2',
    #     ]))
    # print tabulate(table, headers=["Planet","R (km)", "mass (x 10^29 kg)"])





main()
