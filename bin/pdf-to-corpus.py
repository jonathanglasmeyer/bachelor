#!/usr/bin/env python3
 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from pprint import pprint
import re
from pprint import pprint
import os
from os.path import basename
import subprocess
import sys

def call(cmd):
    return subprocess.call(cmd, shell=True)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def main():

    args = sys.argv[1:]

    pdf_filepath = args[0]
    file_basename = os.path.splitext(basename(pdf_filepath))[0]
    output_file_path = '{}.txt'.format(file_basename)
    # os.remove(output_file_path)
    # print(output)

    tmp_corpus_xml = '/tmp/corpus.xml'
    call('pdftohtml -i -xml {} {} &>/dev/null'.format(pdf_filepath, tmp_corpus_xml))
    # get rid ofo bug in pdfreflow
    call('sed -i.bak "s/<pdf2xml.*/<pdf2xml>/g" {}'.format(tmp_corpus_xml))

    # outputs to /tmp/corpus.html
    call('pdfreflow -r {} &>/dev/null'.format(tmp_corpus_xml))

    soup = BeautifulSoup(open('/tmp/corpus.html').read())
    # texts = soup.findAll(text=True)
    # visible_texts = list(filter(visible, texts))
    text_elements = [' '.join(s.extract().text.split('\n')) for s in soup(['p', 'blockquote'])]
    # visible_text = soup.getText()

    tmp_corpus_filename = '/tmp/corpus.txt'
    open('/tmp/corpus.txt', 'w').write('\n'.join(text_elements))
    # call('pandoc /tmp/corpus.html -o {}'.format(tmp_corpus_filename))

    # move to tmp
    # call('cat {} > {}'.format(output_file_path, tmp_corpus_filename))

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
