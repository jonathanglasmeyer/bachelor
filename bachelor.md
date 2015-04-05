---
bibliography: bachelor.bib
title:  'Expose Bachelorarbeit - Augmenting accuray of automatic lecture transcriptions by using context information from slide contents'
author: Jonathan Werner
tags: [NLP]
---
# Abstract
Automatic speech recognition (ASR) of university lectures is an important topic because of two main reasons: 1) providing accessibility for deaf people in the form of subtitles and 2) making the spoken text searchable, thus making it feasible to skim the content efficiently.

The main problem concerning ASR on academic lectures is the error rate for technical terms. This paper explores the possibility of improving recognition accuracy by adapting the vocabulary model with words that are extracted from the speakers slides.

# Motivation
Scannability is crucial for academic research -- but audio/audio-visual sources make this really hard right now. A concrete use case exists at the university of Hamburg, were we have the lecture2go system which makes video recordings of many lectures available. It would be a great benefit for students that want to rewatch the lectures in preperation for an exam to have searchable transcriptions of the lectures. If the results of the augmented transcriptions are good enough they could be rather easily integrated into the lecture2go website and provide an actual benefit to students.

During a project at the University Hamburg in the winter semester 14/15 we implemented a system which automatically generated subtitles for a given audio/video and a transcription. The system that I plan to implement for this thesis will integrate with this project: it would supply the missing first step in the toolchain: automatically generating the transcriptions (For the project we only used human generated transcriptions).

# Work schedule
I would start by testing if and how the open source tool 'CMU Spinx' is able to adapt the recognition process in favor of specific set of words

# Gliederung, konkrete Kapitelnamen
# Absatz, der konkret benennt, wie die Kapitel aufeinander aufbauen

# Literatur
- @cerva2012browsing
- @maergner2012unsupervised
- @miranda2013improving
- @kawa
- @real

# Bibliographie
