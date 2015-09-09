# high level pipeline

`hotword-init testcase_name audio.mp3 transcript.html slide.pdf`
`sphinx-interpolated.py config.json` in `results/$testcase` dir
`sphinx-interpolated.py config.json 1` in `results/$testcase` dir
`hotword-analyze testcase_name`

# under the hood

###. Recognition
1.2 `html-to-corpus transcription.html reference` (will output `reference.corpus.txt`)
1. `pdf-to-corpus.py slides.pdf > slides.corpus.txt`
1.1 (optional: manually edit `slides.corpus.txt`)
2. `estimate-ngram -text slides.corpus.txt -write-lm model.lm`

###. Analysis
1. Cloud visualization
  1.1 `filter.py reference.txt > reference_wordcounts.json`
  1.2. `wordpositions reference_wordcounts.json times.txt > word_timings.json`
  1.3 `cluster.py word_timings.json`
  1.4 copy `word_timings.json` to `viz/public/data/words.json`

2. RWER (Relevant Word Error Rate)
  2.1 `wer.py reference.txt hypothesis.txt > wer-baseline.txt`
  2.2 `wer.py reference.txt hypothesis2.txt > wer-better.txt`
  2.3 `compare-wer.py wer-baseline.txt wer-better.txt name-baseline name-better slide-corpus.txt > wer_comparison.html`

# scripts descriptions

#### `html-to-corpus`
- takes a HTML-File from the resources and transform it to a uppercased, punctuation removed blob of words.
- pass this corpus to filter.py to get the reference word timings

#### `filter.py corpus.txt`:
- take a corpus text (from a reference!), collect all nouns and filter out the top x most common words. (plus variants of those like plurals) (x = 500 right now).
- remove short words (<3 chars) and words with "'" in them
- export those words and their counts into json (stdout)

input: result.txt

#### `sort-word-counts.py <filter.py-output.json>`:
print them words sorted

#### `wordpositions <filter.py-output> <sphinx4run_times.txt>`:
Take a reference words file (output by `filter.py` for a given transcript) and a timing file for a recognition run (from Sphinx) and create a JSON array with words sorted by most often used in reference with found positions.
`wordpositions ~/bachelor-results/2/interesting-words.json ~/bachelor-results/2/psy2_times.txt`

In contrast to evaluating the general WER performance (possible with `wer.py` / `compare-wer.py`) this gives a WER analysis of the performance with respect to potentially more 'interesting' words, as we are only evaluating what the WER of words is that fall below the threshold of the most-common-words filter.

  (NOTE: this tool doesn't actually do this evaluation, but only supplies the necessary data for this task. see `measure-kwer-perf`)


input: `interesting-words.json` and `psy2_times.txt`
output: `positions-frequent-words-500.json`

#### `measure-kwer-performance <output-from-wordpositions>`:
shows overall keyword error rate

#### `cluster.py`:
create clusters for each word (from the output of wordpositions)
-> mutative on the file in place

#### `wer.py reference.txt hyp.txt`:
show general WER analysis with respect to the whole reference text

#### `compare-wer.py wer-baseline.txt wer-better.txt name-baseline name-better slide-corpus.txt`:
compare to WER analysis, output html to stdout with nice formatting

#### `pdf-to-corpus.py class03.pdf`:
the whole chain from open yale supplied slide pdf to corpus file (stdout) ready for manual postprocessing and/or `estimate-ngram`

#### `estimate-ngram -text corpus.txt -write-lm model.lm`:
generate a language model ready for sphinx4

