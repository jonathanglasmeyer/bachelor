#!/usr/bin/env python3
import sys, os, shutil
from os.path import join, isfile
from subprocess import call

script_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.abspath(join(script_path, os.pardir))
results_path = join(project_path, 'results')

config_template = """{{
  "acousticModelPath": "en-new/cmusphinx-en-us-5.2",
  "dictionaryPath": "en-new/cmudict-en-us.dict",

  "languageModelPath": "en-new/cmusphinx-5.0-en-us.lm",
  "keywordModelPath": "model.lm",
  "g2pModelPath": "en-new/en_us_nostress/model.fst.ser",

  "resultsFolder": "{}"
}}
"""


def main():
    args = sys.argv[1:]
    if len(args) < 4:
        print('hotword-init.py testcase_name audio.mp3 transcript.html slide.pdf')
        sys.exit()
    assert len(args) == 4

    testcase_name = args[0]

    audio_file_path = args[1]
    assert audio_file_path.endswith('.mp3')
    assert isfile(audio_file_path)

    transcript_file_path = args[2]
    assert transcript_file_path.endswith('.html')
    assert isfile(transcript_file_path)

    slides_file_path = args[3]
    assert slides_file_path.endswith('.pdf')
    assert isfile(slides_file_path)

    print("Creating new test case with name '{}'".format(testcase_name))
    testcase_dir = join(results_path, testcase_name)

    def call_(cmd):
        return call(cmd, cwd=testcase_dir, shell=True)

    os.mkdir(testcase_dir)
    resources_folder = join(testcase_dir, 'resources')
    os.mkdir(resources_folder)


    audio_dest_file = join(resources_folder, 'audio.mp3')
    transcript_dest_file = join(resources_folder, 'transcript.html')
    slides_destination_file = join(resources_folder, 'slides.pdf')
    config_file_path = join(testcase_dir, 'config.json')

    config = config_template.format(testcase_name)
    shutil.copyfile(audio_file_path, audio_dest_file)
    shutil.copyfile(transcript_file_path, transcript_dest_file)
    shutil.copyfile(slides_file_path, slides_destination_file)
    open(config_file_path, 'w').write(config)

    # build keyword model

    call_('pdf-to-corpus.py resources/slides.pdf > slides.corpus.txt')
    call_('estimate-ngram -text slides.corpus.txt -write-lm model.lm')
    call_('html-to-corpus resources/transcript.html reference') # (will output `reference.corpus.txt`)

    call_('ffmpeg -i resources/audio.mp3 -acodec pcm_s16le -ar 16000 -ac 1 resources/audio.wav')

    # for later cluster analysis
    call_('filter.py reference.corpus.txt > reference_wordcounts.json')

    # manual:
    # [3] `sphinx-interpolated.py config.json`
    # [4] `sphinx-interpolated.py config.json 1` for interpolated

    # after sphinx...
    # call_('wordpositions reference_wordcounts.json times.txt > word_timings.json')

main()
