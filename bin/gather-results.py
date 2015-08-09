#!/usr/bin/env python2
from __future__ import division
from json2html import *
from tabulate import tabulate
import sys, os, json
from pprint import pprint

from os.path import join, isfile

# string constants
EMPTY = '.'

# flags
PRINT_HTML = True

def log(s):
    if not PRINT_HTML:
        pprint(s)

script_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.abspath(join(script_path, os.pardir))
template_folder = os.path.join(script_path, 'data/html_template')
results_path = join(project_path, 'results')

COLUMNS = [
    ('name', 'Name', '', 1),
    ('W', '# W', '# of words in reference', 0),
    ('IW', '# IW', '# of interesting words in reference', 1),

    ('WER_A', 'WER<sub>A</sub>', 'Word Error Rate of baseline (A)', 0),
    ('WER_B', 'WER<sub>B</sub>', 'Word Error Rate of interpolated run (B)', 0),

    ('W_worse', 'W<sub>worse</sub>', 'W that have been recognized in (A) but not in (B). Together with W_improved it explains the improvement from WER_A to WER_B', 0),
    ('W_improved', 'W<sub>improved</sub>', 'W that have not been recognized in (A) but have been in (B)', 1),


    ('IWER_A', 'IWER<sub>A</sub>', 'Interesting Word Error Rate of baseline (A)', 0),
    ('IWER_B', 'IWER<sub>B</sub>', 'Interesting Word Error Rate of interpolated run (B)', 0),

    ('IW_worse', 'IW<sub>worse</sub>', 'IW that have been recognized in (A) but not in (B). Together with IW_improved it explains the improvement from IWER_A to IWER_B', 0),
    ('IW_improved', 'IW<sub>improved</sub>', 'IW that have not been recognized in (A) but have been in (B)', 1),

    ('W_worse_I', 'W<sub>worse</sub>(I)', 'Amount of worsened words that were interesting.  This is the key quality indicator of the interpolation run ', 0),
    ('W_improved_I', 'W<sub>improved</sub>(I)', 'Amount of improved words that were interesting.  This is the key quality indicator of the interpolation run ', 1),
]

for c in COLUMNS:
    assert(len(c) == 4)

def cellStyle(shouldHaveRightBorder):
    return 'rightBorder' if shouldHaveRightBorder else ''

def header(columns):
    return '<tr>\n\t{}\n</tr>\n'.format('\n'.join(
        ['<th class="{}" title="{}">{}</th>'.format(cellStyle(shouldHaveRightBorder), description, caption) 
            for (_, caption, description, shouldHaveRightBorder) in columns]))


def row(columns):
    return '<tr>\n\t{}\n</tr>\n'.format('\n'.join(['<td class="{}">{}</td>'.format(
        cellStyle(shouldHaveRightBorder), c) for (c, shouldHaveRightBorder) in columns]))

def main():
    # setup resources
    css = open(os.path.join(template_folder, 'style.css')).read()
    template = open(os.path.join(template_folder, 'template.html')).read()

    out = []

    subdirs = os.listdir(results_path)
    results = []
    for resultDir in subdirs:
        resultFile = join(resultDir, 'results.json')
        resultsExist = isfile(resultFile)
        if resultsExist:
            result = json.load(open(resultFile))
            result['name'] = resultDir
            results.append(result)

    # print(json.dumps(results, sort_keys=True, indent=2, separators=(', ', ': ')))

    out.append('<table>')
    out.append(header(COLUMNS))

    def stylePercentage(column):
        if '%' in str(column):
            absolute_values, _, percent = column.split()
            return '<span title="{}">{}</span>'.format(absolute_values, percent)
        else:
            return column

    for result in results:
        log(result)
        column_values = [result.get(key, EMPTY) for (key, _, _, _) in COLUMNS]
        column_values = map(stylePercentage, column_values)
        out.append(row(zip(column_values, [shouldHaveRightBorder for (_, _, _, shouldHaveRightBorder) in COLUMNS])))

    out.append('</table>')

    if PRINT_HTML:
        print(template.format('Summary', css, '\n'.join(out)))


main()
