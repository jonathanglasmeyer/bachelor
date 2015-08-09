#!/usr/bin/env python3
import sys, os, json
from os.path import join, isfile
from subprocess import call
script_path = os.path.dirname(os.path.realpath(__file__))

TOC_FILE = 'TOC.txt'
OUT_FILE = 'out/bachelor.pdf'

def wrapInQuotes(s):
    return '"{}"'.format(s)

def call_(cmd):
    print(cmd)
    return call(cmd, cwd=script_path, shell=True)

def main():
    toc = open(join(script_path, 'TOC.txt')).read().split('\n')
    files = ['src/{}.md'.format(basename) for basename in toc if basename]


    call_('pandoc -t latex -o {outfile} --filter pandoc-citeproc {files}'.format(
        outfile=OUT_FILE,
        files=' '.join(map(wrapInQuotes, files))
    ))

main()
