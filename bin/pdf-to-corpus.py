#!/usr/bin/env python3
 # -*- coding: utf-8 -*-
from pprint import pprint
import os
from os.path import basename
import subprocess
import sys

def call(cmd):
    return subprocess.call(cmd, shell=True)

def main():
    args = sys.argv[1:]

    pdf_filepath = args[0]
    file_basename = os.path.splitext(basename(pdf_filepath))[0]
    output_file_path = '{}.txt'.format(file_basename)
    # os.remove(output_file_path)
    # print(output)

    tmp_corpus_filename = '/tmp/corpus.txt'
    call('pdftotext {}'.format(pdf_filepath))

    # move to tmp
    call('cat {} > {}'.format(output_file_path, tmp_corpus_filename))

    # collapse ' (eg freud's to freuds)
    call("""sed -i.bak "s/[’']//g" {}""".format(tmp_corpus_filename))

    call('cat {} > {}'.format(tmp_corpus_filename, output_file_path))


    # use the tocorpus tool to clean up
    call('cat {} | tocorpus.pl > {}'.format(
        output_file_path, tmp_corpus_filename))

    os.remove(output_file_path)

    # only alphabetical characters

    call("sed -i.bak 's/[^a-zA-Z]/ /g' {}".format(tmp_corpus_filename))
    # remove empty lines
    call("sed -i.bak '/^\s*$/d' {}".format(tmp_corpus_filename))

    # remove more than one contiguous space
    call("sed -i.bak 's/  */ /g' {}".format(tmp_corpus_filename))

    # remove leading whitespace
    call("sed -i.bak 's/^  *//g' {}".format(tmp_corpus_filename))

    result = open(tmp_corpus_filename).read()
    result = result.lower()
    print(result)




main()
