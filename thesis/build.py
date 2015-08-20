#!/usr/bin/env python3
import sys, os, json
from os.path import join, isfile
from subprocess import call
script_path = os.path.dirname(os.path.realpath(__file__))

TOC_FILE = 'TOC.txt'
OUT_FILE = 'out/bachelor.pdf'

def flatten(l):
    return [item for sublist in l for item in sublist]

def wrapInQuotes(s):
    return '"{}"'.format(s)

def call_(cmd):
    print(cmd)
    return call(cmd, cwd=script_path, shell=True)

def main():
    toc = [l for l in open(join(script_path, 'TOC.txt')).read().split('\n') if l]
    # for basename in toc:
    #     open('/tmp/{}.md'.format(basename), 'w').write('\n# {}\n'.format(basename) if not basename.startswith('_') else '\n\n')

    # files = flatten([['/tmp/{}.md'.format(basename), 'src/{}.md'.format(basename)] for basename in toc])
    files = ['src/{}.md'.format(basename) for basename in toc]
    print('files: {}'.format(files))

    call_('pandoc -t latex -o {outfile} --number-sections --filter pandoc-citeproc {files}'.format(
        outfile=OUT_FILE, files=' '.join(map(wrapInQuotes, files))
    ))

print('Building...')
main()


