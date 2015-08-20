<!-- Task: the Introduction basically talks about the whole project at a high level from top to bottom. --!>

# Introduction
Scannability is crucial for academic research: you have to be able to quickly evaluate the usefulness of a given resource by skimming the content and looking for the parts that are specifically relevant to the task at hand.

The medium in which those resources are available is very centered on textual representation. Spoken content, hereinafter called **speech media** (audio- or audiovisual media that mainly consists of spoken language) **doesn't make it possible to scan its contents.** You are "stabbing in the dark" when looking for something specific in a medium like this and have to consume it like a linear narrative.

This means that although lectures and conference talks are a central element to science they are much more challenging and tedious to use for research work.

Being able to a) efficiently **search** and b) look at the **temporal distribution of important keywords** in a visually dense way would elevate the usefulness of speech media in the scientific context immensely.

One approach to accomplish those goals is utilizing Automatic Speech Recognition (ASR) to transcribe speech to text and also get timing information for the recognized words. This makes it possible to derive information about the density of given words at a given point of time in the talk, which in turn allows to compute **word occurence density maxima**. This opens up possibilities for **compact visual representation** of the interesting keywords, thus allowing the user to **scan**.

The main challenge when using ASR for this task is the recognition accuracy of technical terms. Most of them are not included in the language models that are available as those are broad and generic so as to optimize for accuracy over a wide topic spectrum. But when they are not included into the language model they have no chance to be correctly recognized at all.  <!-- Is this absolutely true?  --!>

So the usefulness of applying ASR with a generic language model to the problem is very small, as the intesection of interesting keywords with those technical terms that can not be recognized is very big.

The central goal of this thesis is to explore an approach to overcome this problem. This approach consists of using words from lecture slides or other notes to **generate a lecture-specific language model**. This is then **merged** with a generic language model and being compared to the 'baseline' accuracy of the generic model.

<!-- High level overview of the proposed process & the implementation --!>
## Structure of this thesis
I will now describe the structure of this thesis.




<!-- High level overview of the proposed metrics --!>

<!-- Summary: research questions --!>

<!-- Summarize research questions --!>

<!--



A live example of this idea can be seen at superlectures.com ^[http://www.superlectures.com/sigdial2014/welcome-and-conference-overview-1]. They present transcripts generated via automatic speech recognition, aligned to the video in a searchable text box beneath the video player. The main problem here is the bad recognition accuracy of technical terms, which diminishes the value of this solution: scanning the text is actually less effective than 'scanning the video' as the false-positives are confusing.
 --!>

<!--
## Lecture recordings in universities
## Speech recognition accuracy problems with special words / technical terms
## Goal: improving searchability / scannability through adapting language models
--!>

# Background
<!--
- ASR in general, state of the art
- Language models, acoustic models
  - Trigram
- Log10 format, ARPA, example

- Scientific work in this field
  - compare different approaches, acoustic model vs language model adaption
  - typical metrics: WER, proposed alternatives to WER


--!>

# Methodology

<!--
## From the goal of searchability to good metrics
- Why keywords are important for searching ( obvious?)
- Find a metric that represents the quality of the keyword recognition accuracy
- Find a metric that describes how well a method performs in improving the accuracy for keywords compared to a baseline


## Selection of lectures
- Open Yale
- why

--!>
# Process
# Discussion and Findings
# Improvements
# Conclusions
