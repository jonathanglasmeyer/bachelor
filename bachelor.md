---
bibliography: bachelor.bib
title:  'Expose Bachelorarbeit - Augmenting accuracy of automatic lecture transcriptions by using context information from slide contents'
author: Jonathan Werner
tags: [NLP]
---
# Abstract
Automatic speech recognition (ASR) of university lectures is an important topic because of two main reasons:
1) providing accessibility for deaf people in the form of subtitles and
2) making the spoken text searchable, thus making it feasible to skim the content efficiently.

The main problem concerning ASR on academic lectures is the error rate for technical terms.
This paper explores the possibility of improving recognition accuracy by adapting the vocabulary model with words that are extracted from the speakers slides.

# Motivation
Scannability is crucial for academic research -- but audio/audio-visual sources make this really hard right now.
A concrete use case exists at the university of Hamburg, were we have the *lecture2go* system which makes video recordings of many lectures available.
It would be a great benefit for students that want to rewatch the lectures in preperation for an exam to have searchable transcriptions of the lectures. If the results of the augmented transcriptions are good enough they could be rather easily integrated into the *lecture2go* website and provide an actual benefit to students.

During a project at the University Hamburg in the winter semester 14/15 we implemented a system which automatically generated subtitles for a given audio/video and a transcription.
The system that I plan to implement for this thesis will integrate with this project.
It would supply the missing first step in the toolchain: automatically generating the transcriptions (for the project we only used human generated transcriptions).

# Work schedule
I will start by testing if and how the open source tool 'CMU Spinx' is able to adapt the recognition process in favor of a specific set of words.

I will then start implementing a prototype pipeline which extracts textual content from slide pdfs and feeds them into CMU Sphinx.
This has the goal of finding out which parts would have to be manually implemented and which parts are already available. I would estimate that I need about one month of time to have a working software prototype.

I will then start measuring if the given process is able to increase recognition accuracy. I will compare the results to the results obtained by the papers listed below. I would give this part another month. I would reserve the last month for polishing the general quality of the paper.

# Paper structure
A first approach for the structure could look like this:

1. Introduction
    1. Comparison to related works
2. Pipeline Overview
3. Modules
4. Measurements, Analysis
5. Conclusion

I will start with a summary of the problem space and the proposed solution. I will summarize related work and the different approaches that the authors explored.

I will then give a high-level overview over my implementation, followed by a detailed explanation about the modules and their interaction. This will include an extensive part about the internal workings of the adaption process during the ASR phase and comparisons and differences to the approaches outlined in the papers below.

I will then analyze the results and compare the recognition accuracy of the implementation with baseline measurements.

Finally I will close with a summary and a conclusion about the value of the proposed solution.

# Literature
I plan to use the following literature:

- @cerva2012browsing
- @maergner2012unsupervised
- @miranda2013improving
- @kawa
- @real

# Bibliography
