<!-- Task: the Introduction basically talks about the whole project at a
high level from top to bottom. --!>

\newpage

# Introduction {-}
Scannability is crucial for academic research: you
have to be able to quickly evaluate the usefulness of a given resource
by skimming the content and looking for the parts that are specifically
relevant to the task at hand.

The medium in which those resources are available is very centered on
textual representation. Spoken content, hereinafter called *speech
media* (audio- or audiovisual media that mainly consists of spoken
language) doesn't make it possible to scan its contents. You are
"stabbing in the dark" when looking for something specific in a medium
like this and have to consume it like a linear narrative.

This means that although lectures and conference talks are a central
element to science they are much more challenging and tedious to use for
research work.

Being able to a) efficiently search and b) look at the temporal
distribution of important keywords in a visually dense way would
elevate the usefulness of speech media in the scientific context
immensely.

One approach to accomplish those goals is utilizing Automatic Speech
Recognition (ASR) to transcribe speech to text and also get timing
information for the recognized words. This makes it possible to derive
information about the density of given words at a given point of time in
the talk, which in turn allows to compute word occurence density
maxima. This opens up possibilities for compact visual
representation of the interesting keywords, thus allowing the user to
scan.

The main challenge when using ASR for this task is the recognition
accuracy of technical terms. Most of them are not included in the
language models that are available as those are broad and generic so as
to optimize for accuracy over a wide topic spectrum. But when they are
not included into the language model they have a very small chance to be correctly
recognized at all.  <!-- TODO: maybe account for smoothing here? --!>

So the usefulness of applying ASR with a generic language model to the
problem is very small, as the intersection of interesting keywords with
those technical terms that can not be recognized is very big.

The central goal of this thesis is to explore an approach to overcome
this problem. This approach consists of using words from lecture slides
or other notes to generate a lecture-specific language model. This
is then interpolated with a generic language model and being
compared to the 'baseline' accuracy of the generic model.

\pagebreak

## Structure of this thesis {-}
The structure of this thesis is laid out as follows:

(#) **Research questions**

    I will state the research questions.

(#) **Scientific Background**

    #. I will start by giving an overview over the state of the art of
    ASR and the most prevalent approaches.

    #. I will explain the *concepts* which are fundamental for the
    understanding of speech recognition.

    #. I will then examine the *scientific work* that has been done on
    applying ASR to the problem of lectures transcriptions.

    #. Finally i will summarize the *metrics* that have been used to
    assess the quality of the improvements in different approaches.

(#) **Motivation**

    Here i will motivate why it is necessary to improve on the baseline performance of ASR in our context.

    I will talk about the role of keywords and technical terms and why they are not being detected and how that diminishes the usefulness of ASR for the purposes of scannability.

(#) **Test data**

    I will use the openly available *Open Yale Courses* @openyale, which provide a
    diverse selection of audio and video recordings of university lectures at Yale, additionally supplying quality manual transcriptions and course notes or slides.

    I will present the chosen courses, their selection criteria and
    discuss the range of types of lecture material.

(#) **The LM-Interpolation approach**

    #. **Technical basis**

        I will introduce the open source speech recognition framework
        *Sphinx 4*. This is the software that is used for performing the
        actual recognition.

    #. **Process overview**

        I will then give a overview of the design and architecture of
        our approach.

    #. **Implementation**

        Finally i will describe the technical implementation by which the
        lecture material is compiled into a specialized language model
        and recognition is performed using a *interpolated* language
        model.

(#) **Analysis**

    #. **Methods**

        I will discuss how to analyze the results and develop metrics
        that assess how well the given goals are met with our approach.
        <!-- TODO: which metrics follow from the goals of searchability and
        scannability.  define those terms first, discuss what's
        important there ->> keywords! --!>

    #. **Analysis**

        I will then perform quantitative analysis on our test dataset
        with the metrics we developed before.

    #. **Discussion, Finding and Conclusions**

        I will discuss the findings and draw conclusions from the quantitative analysis concerning the effectiveness of our approach.

(#) **Visualization for Scannability**

    I will present a prototype visualization method that uses the results from our approach to present a condensed representation of the keyword content from lectures with the goal of providing a quick, interactive way to search and scan speech media.

(#) **Improvements, Open Ends**

    I will discuss possible improvements and open ends that were out of
    the scope of this thesis but would be interesting to explore further.

(#) **Summary**

    I will end by summarizing the goals, the proposed approach, the
    design and implementation, the analysis and the results.

\pagebreak

# Research questions
The central research questions i want to investigate in this thesis can
be formulated as follows:

(#) When we apply ASR to university lectures, what is the advantage of using an approach that consists of creating a lecture-specific language model and interpolating it with a generic language model, given that we are interested in improving the recognition accuracy of *interesting keywords* for the sake of
searchability and scannability?

(#) What metric is useful for quantifying this advantage?

A secondary question is: How can we *use* the results from our approach to provide graphical interfaces for improving the users ability to search and scan the given speech medium?

The exploration of this question will not be the center of this thesis,
but it will provide practical motivation for the results that the
exploration.


<!-- ## Lecture recordings in universities ## Speech recognition
accuracy problems with special words / technical terms ## Goal:
improving searchability / scannability through adapting language models
--!>

# Background

## The field of Automatic Speech Recognition
Automatic Speech Recognition (ASR) can be defined as the process by which
a computer maps an acoustic speech signal to text @cmufaq.

@rabiner date the first research on ASR back to the
early 1950s, when Bell Labs built a system for single-speaker digit
recognition. Since then the field has seen three major approaches, which
@marquard summarizes as follows:

> 1. The *acoustic-phonetic approach* aimed to identify features of
    speech such as vowels directly through their acoustic properties,
    and from there build up words based on their constituent phonetic
    elements.

> 2. The *statistical pattern-recognition approach* measures features of
    the acoustic signal, and compares these to existing patterns
    established from a range of reference sources to produce similarity
    scores which may be used to establish the best match.

> 3. *Artificial intelligence (AI) approaches* have been used to integrate
    different types of knowledge sources (such as acoustic, lexical,
    syntactic, semantic and pragmatic knowledge) to influence the output
    from a pattern-recognition system to select the most likely match.

<!-- TODO: probably rephrase? --!>

The most prevalent approach today is the *statistical
pattern-recognition approach*, as it produces results with much higher
accuracy compared to the acoustic-phonetic approach. The use of Hidden Markov Models (HMM) has been playing a key role in this approach, as it allows recognizers to use a statistical model of a given pattern rather than a fixed representation.

In the last years there has been a resurgence of AI approaches, specifically *deep learning approaches* [@hinton2012deep]. The ASR paradigm we will use for this thesis will be limited to the former, however.

## Dimensions of speech recognition
There are three dimensions which serve to classify different applications of speech recognition [@cmufaq, @marquard]:

(1) **Dependent vs. independent**. Dependent recognition systems are developed to be used by one speaker, whereas independent systems are developed to be used by *any* speaker of a particular type, i.e North-American speakers. **Adaptive** systems lie between those poles, they are able to adapt to a particular speaker through training.

(2) **Small vs. large vocabulary**. Small vocabularies contain only up to a few hundred words and might be modeled by an explicit grammar, whereas large vocabularies contain tens of thousands of words so as to be able to model general purpose spoken language over a variety of domains.

(3) **Continuous vs. isolated speech**. Isolated speech consists of single words that are spoken with pauses in between them, whereas continuous speech consists of words that are spoken in a connected way. Continuous speech is significantly more difficult to recognize, as it is a) more difficult to find the start and end of words and b) the pronunciation of words changes in relation to their surrounding words.

With those three dimensions we can for example classify the application areas command and control systems, dictation and lecture transcription [@marquard]:

```{.table type="pipe" aligns="LLLL" caption="Three application areas" header="yes"}
Application,                Speaker,     Vocabulary, Duration
Dictation,                  Dependent,   Large,      Connected
Command and control system, Independent, Small,      Isolated
Lecture transcription,      Independent, Large,      Connected
```

The task of automatic lecture transcriptions can thus be characterized as speaker-independent (SI) large continuous speech recognition (LVCSR).

## Concepts
Speech recognition in the *statistical pattern-recognition approach* paradigm has three major concepts necessary for its understanding:

* phonemes and phonetic dictionaries
* acoustic models (AM)
* language models (LM)

### Phonemes
A *phoneme* is "the smallest contrastive linguistic unit which may bring about a change of meaning" [@cruttenden2014gimson, p. 43]. They are the smallest unit of sound in speech which are combined to form words. The word *sun* for example can be represented by the phonemes `/s/`, `/u/` and `/n/`; the word *table* by `/t/`, `/a/` and `/bl/`.

A language together with a specific accent can be described by a set of phonemes that it consists of. Figure \ref{phonemic-chart} uses symbols from the International Phonetic Alphabet (IPA) to display the 44 phonemes that are being used in Received Pronunciation (RP), which is regarded as the "standard accent" in the south of the United Kingdom [@stevenson2011concise].

![Phonemic Chart representing 44 phonemes used in RP British English\label{phonemic-chart}](images/phonemes_50.jpg)

To be able to use phonemes in software an ASCII representation is more suitable. The standard for General American English is the *Arpabet*. Here each phoneme is mapped to one or two capital letters. The digits `0`, `1` and `2` signify stress markers: no stress, primary and secondary stress respectively. A comparison of the IPA format and the arphabet format can be seen in Figure \ref{arpabet}, an excerpt that just shows the *monophthongs* ^[pure vowel sounds with relatively fixed articulation at the start and the end that don't glide towards a new position of articulation].

![Excerpt from the Arpabet @wikiArpabet \label{arpabet}](images/arpabet.png)

### Phonetic dictionaries

Phonetic dictionaries map words to one or multiple versions of phoneme sequences.

A phonetic representation of a word is specified manually from the knowledge how written words *actually sound* when spoken.

An excerpt from the dictionary `cmudict-en-us.dict` @cmuDict looks like this:

    ...
    abdollah AE B D AA L AH
    abdomen AE B D OW M AH N
    abdomen(2) AE B D AH M AH N
    abdominal AE B D AA M AH N AH L
    abdominal(2) AH B D AA M AH N AH L
    ...

The dictionary has 133.425 entries. In the general case only words that are in the phonetic dictionary being used can be recognized during speech recognition. *Grapheme^["The smallest unit used in describing the writing system of a language" @florian1996blackwell, p.174]-to-Phoneme converters* (G2P) however make it possible to get phoneme sequence hypotheses for arbitrary words (that meaning arbitrary sequences of graphemes). While those results are on average less accurate than manually created variants, they play a vital role in texts with many technical terms as those are often not part of phonetic dictionaries.

### Acoustic models
An acoustic model (AM) describes the relation between an audio signal and the probability that this signal represents a given phoneme.

Acoustic models are created by *training* them on a *corpus* of audio recordings and matching transcripts. When being used in the context of speaker-independent recognition, those models are trained with a variety of speakers that represent a broad spectrum of the language/accent that the acoustic model should represent.

During the *decoding* phase the acoustic model and a phonetic dictionary are used to match sequences of small audio "slices" to possible phonemes and those phonemes to possible word sequence hypotheses. <!-- TODO: oohoo. is this precise? --!>

However, acoustic models alone are not sufficient for speech recognition as they don't have the "higher-level" linguistic information necessary to for example decide between homonyms and similar-sounding phrases such as "wreck a nice beach" and "recognize speech" [@marquard, 11]. This information finally is provided by *language models*.

### Language Models

Language models (LM) guide and constrain the search process a speech recognition system performs by assigning probabilities to sequences of words. They are trained by applying statistical methods on a text corpus. <!-- TODO: mh. awkward --!> Analogous to acoustic models, generic language models use huge text corpora with a broad variety of topics. It is however possible to train language models on small and specialized text corpora, which is the central technical foundation for the approach discussed in this thesis.

The most commonly used form of language models are *n-gram language models*. In the context of a language model a *n-gram* is a sequence of *n* words. 1-grams are called *unigrams*, 2-grams are called *bigrams* and 3-grams are called *trigrams*. A *n-gram language model* maps a set of *n-grams* to probabilities that they occur in a given piece of text.

A key idea in modelling language like this is the *independence assumption*, which says that the probability of a given word is only dependent on the last *n* - 1 words. This assumption significantly decreases the statistical complexity and makes it thus computationally feasible.

N-gram language models don't need to be constrained to one type of n-gram. The *Generic US English Generic Language Model* @cmuLm from CMUSphinx we will use as the baseline for our approach for example consists of 1-, 2, and 3-grams.

A toy example of a language model with 1- and 2-grams when represented in *ARPA*-format (as used by CMUSphinx) looks like follows @cmuArpa:

    \data\
    ngram 1=7
    ngram 2=7

    \1-grams:
    -1.0000 <UNK>	-0.2553
    -98.9366 <s>	 -0.3064
    -1.0000 </s>	 0.0000
    -0.6990 wood	 -0.2553
    -0.6990 cindy	-0.2553
    -0.6990 pittsburgh		-0.2553
    -0.6990 jean	 -0.1973

    \2-grams:
    -0.2553 <UNK> wood
    -0.2553 <s> <UNK>
    -0.2553 wood pittsburgh
    -0.2553 cindy jean
    -0.2553 pittsburgh cindy
    -0.5563 jean </s>
    -0.5563 jean wood

    \end\

Here the first number in a row is the probability of the given n-gram in $log_{10}$ format. This means that the unigram *wood* has a probability of $10^{-0.6990} \approx 0.2 = 20\%$ and the probability of the words "wood pittsburg" occuring in sequence is $10^{-0.2553} \approx 0.55 = 55\%$ .

The optional third numeric column in a row is called *backoff weight*. Backoff weights make it possible to calculate n-grams that are not listed by applying the formula

    P( word_N | word_{N-1}, word_{N-2}, ...., word_1 ) =
    P( word_N | word_{N-1}, word_{N-2}, ...., word_2 ) *
      backoff-weight( word_{N-1} | word_{N-2}, ...., word_1 )

With the side condition that missing entries for `word_{N-1} | word_{N-2}, ...., word_1` are replaced by $1.0$.

So if the text to be recognized would contain the sequence "wood cindy", which does not appear as a bigram in the LM, the probability for this bigram could be calculated by `P(wood|cindy) = P(wood) * BWt(cindy)`.

Finally, the overall probability of a sentence with the words $w_1,...,w_n$ can be approximated as follows:

$$P(w_1,...,w_n) = \prod_{n=1}^m P(w_i \mid w_1,...w_{i-1})$$

An example approximation with a bigram model for the sentence "I saw the red house" @wikiLM represented as $P(\text{I, saw, the, red, house})$ would look like
$$
  P(\text{I} \mid \langle s \rangle) \times
  P(\text{saw} \mid \text{I}) \times
  P(\text{the} \mid \text{saw}) \times
  P(\text{red} \mid \text{the}) \times
  P(\text{house} \mid \text{red}) \times
  P(\langle s \rangle \mid \text{house})
$$

<!-- TODO: überleitun? --!>

## Work done on ASR for lecture transcription

I will now give an overview over the scientific work done on lecture transcription, using @marquard as a guiding reference.

The research for speech recognition on lectures can be partitioned into three general approaches: generalization approaches, specialization approaches and approaches involving the user for manual correction and improvements.

### Generalization approaches
Generalization approaches try to create models that capture common characteristics of lectures. Those characteristics include highly spontaneous presentation style and "strong coarticulation effects, non-grammatical constructions, hesitations, repetitions, and filled pauses" [@yamazaki]. @glass note the "colloquial nature" of lectures as well as the "poor planning at the sentence level [and] higher structural levels".

The generalization approach has been applied on the acoustic model level: @cettolo have examined adapting a generic acoustic model to account for spontaneous speech phenomena ("filler sounds"). <!-- TODO: formulierung --!>

While the a subfield of ASR called "speaker diarization" tries to account for the interactivity between lecturers and students by identifying multiple speakers, most research treats lectures as single speaker events with the audience as background noise.

Generalization approaches at the language model level try to model common linguistic traits of the lecture genre (this can be called the "macro level"). @kato2000 investigate topic-independent language modeling by creating a large corpus of text from lecture transcripts and panel discussions and then removing topic-specific keywords. ^[In a second step they combine this generalization technique with a specialization technique by adapting the resulting LM with a lecture-specific language model by using preprint papers of a given lecture.]

### Specialization approaches
Specialization approaches try to use context specific to a single lecture ("meso level") or parts of a single lecture ("micro level"^[The three levels are taken from @marquard.]).

Methods used for creating LMs from context information can be categorized into two approaches: direct usage of lecture slides and notes for the creation of LMs versus usage of "derived" data from those materials. Deriving data by using keywords found in slides, using them as web search query terms and using the found documents as the basis for LM creation is explored in @munteanu, @kawahara08 and @marquard.

Using the whole text from lecture slides has been explored by @yamazaki. They compare the *meso level* with the *micro level* by dynamically adapting the LM for the speech corresponding to a particular slide. <!-- TODO: results? --!> @kawahara08  also examine dynamic local slide-by-slide adaption and compare it to global topic adaption using Probabilistic Latent Semantic Analysis (PLSA)^[Latent Semantic Analysis is an approach to document comparison and retrieval which relies on a numeric analysis of word frequency and proximity. <!-- TODO: reformulate --!>] and web text collection, concluding that the last performs worse then the former because of a worse orientation to topic words. <!-- TODO: find citation that is not from marquard --!>.

<!--
@akita (todo):

    statistical transformation model for adapting a pronunciation model
    and LM from a text corpus primarily reflecting written language to
    one more suited for recognizing spoken language.

    While n-gram language models are the dominant paradigm in ASR
    systems, they offer a relatively coarse model of language context.

“The sequence
memoizer,”
    Newer research is exploring more accurate statistical representations
    of “deep context”, for example accounting for connections between
    related but widely separated words and phrases [41].

 --!>
<!-- TODO: finish this crap --!>

## Metrics

<!-- TODO: finish this crap --!>

# Test data

42 courses
The test data i will use for evaluating our approach will be from *Open Yale Courses*^[[http://oyc.yale.edu/](http://oyc.yale.edu/)], which is a selection of openly available lectures from Yale university. It consists of 42 courses from 25 departments. Each course has about 20-25 sessions that have an average length of 50 minutes. Each lecture is provided with good quality audio and video recordings, precise manual transcripts and lecture material when available. Only about 20% of the lecture have lecture notes or slides at all and most materials from the natural and formal science departments (physics, astronomics, mathematics) consist of hand-written notes, making them unsuitable for our approach. All talks are in English.

I have chosen the following lectures: (Department, Course, Lecture Number - Title, abbreviation)

- *Biomedical Engineering*: Frontiers of Biomedical Engineering, 1 - What is Biomedical Engineering?  (`biomed-eng-1`)

- *Environmental Studies*: Environmental Politics and Law, 8 - Chemically Dependent Agriculture (`environmental-8`)

- *Geology & Geophysics*: The atmosphere, the ocean, and environmental change, 8 - Horizontal transport (`geology-8`)

- *Philosopy*: Philosophy and the science of human nature, 8 - Flourishing and Detachment (`human-nature-8`)

- *Psychology*: Introduction to Psychology, 14 - What Motivates Us: Sex (`psy-14`)

- *Psychology*: Introduction to Psychology, 5 - What Is It Like to Be a Baby: The Development of Thought (`psy-5`)

The main selection criterion here was topical diversity, with the challenge that the majority of talks with computer-parsable notes was from the humanities.

## Materials overview
The available material is very heterogeneous. I will now give an overview with excerpts which will serve as a basis for examining later if the quality and quantity of the supplied material is correlated with the amount of improvement of our approach.

`geology-8` supplies a 2-page excercise sheet.

> "Mars has a radius of 3.39 x 106 m and a surface gravity of 3.73 ms-2. Calculate the escape velocity
> for Mars and the typical speed of a CO2 molecule (assume T = 250 K). How can Mars retain its CO2
> atmosphere? (Hint: the molecular weight of carbon dioxide is 44. Use the formulae given in class.) [...]"

`biomed-eng-1` provides a 7-page glossary of technical terms.

> "[...] active transport - the transport of molecules in an energetically unfavorable direction across a membrane coupled to the hydrolysis of ATP or other source of energy
>
> ATP (adenosine 5’-triphosphate) - a nucleotide that is the most important molecule for capturing and transferring free energy in cells. Hydrolysis of each of the two high-energy
> phosphoanhydride bonds in ATP is accompanied by a large free-energy change ("G) of 7
> kcal/mole
>
> aquaporin – a water channel protein which allows water molecules to cross the cell
> membrane much more rapidly than through the phospholipid bilayer [...]"

`human-nature-8` provides reading assignments for four books with short summaries each.

> "[A] Epictetus, The Handbook
>
> Background information about the Stoic philosopher Epictetus (c. 50-130 CE) and his famous
> work Encheiridion (The Handbook) appears in Nicholas White’s introduction to our translation.
> White has also added footnotes that explain points of potential confusion.
>
> As the title indicates, The Handbook is intended as a tidy introduction to a more complex
> philosophical outlook. It is written in an accessible and engaging style.
>
> The Stoic movement originated around 300 BCE and flourished for over five hundred years. The
> Stoics believed that the external world is deterministic: its state at any time is completely
> determined by its prior states. So, they maintained, it is pointless to wish for things to be different
> because to do so is to wish for something impossible. A wise person would, therefore, accept
> whatever befalls them without desiring that things go otherwise – hence the English word ‘stoic.’

> Passages to focus on/passages to skim
>
> I encourage you to read the text in full, at a steady reading pace. [...]"

`psy-14/5` and `enviromental-8` provide ~10-page slides with a typical amount of text.

### Conclusion
Only about 20% of the courses have lecture material at all; only about 20% of those actually have typical "slides" -- the rest provides heterogenous other kinds of material. While it can not be inferred from this dataset that this is a general condition, it nevertheless shows a clear "real-world" disadvantage of an approach only relying on those materials. We will look at the impact of the varying quality and quantity in the analysis later.

# The LM-Interpolation approach
I will now describe the LM-Interpolation approach. The high level overview looks like the following: we will use the open source speech recognition framework Sphinx 4 ^[Homepage: <http://cmusphinx.sourceforge.net/wiki/sphinx4:webhome>] as the software for performing speech recognition. Sphinx 4 has a modular architecture which allows specifying components of the whole process per configuration. It provides multiple implementations of LMs^[Overview: <http://cmusphinx.sourceforge.net/doc/sphinx4/edu/cmu/sphinx/linguist/language/ngram/LanguageModel.html>], the default one being an ngram model.

It also provides an `InterpolatedLanguageModel`^[Javadoc: <http://cmusphinx.sourceforge.net/doc/sphinx4/edu/cmu/sphinx/linguist/language/ngram/InterpolatedLanguageModel.html>] (ILM), which allows you to specify multiple LMs and weights and interpolate the probabilities for a given ngram from all models probabilities ($p = w_1*p_1 + w_2*p_2 + \ldots$ where $w_n$ are the weights ($\sum_{i=1}^n(w_i) = 1$) and $p_n$ are the probabilities from the $n$ LMs for a given word).

The ILM's use in our approach is to factor in the importance of keywords. Those keywords have to be supplied in the form of an ngram language model. For this we extract text content from the lecture material, preprocess it and create an ngram LM from the resulting corpus. Sphinx4 is then a) run with a generic english ngram LM only and b) with the ILM configured to use the generic english LM and the keyword language model in a 50/50 weighting. Finally the two resulting transcriptions are compared with a selection of metrics.

As an example, the 1-gram *sex* has a probability of 2.82% in the keyword model from `psy-14`, but a probability of 0.012% in the generic english LM ^[@cmuLm]. When applying 50/50 interpolation, the result is $2.82\%*0.5 + 0.012\%*0.5 = 1.416\%$, which is an increase by the factor of ~117 over the generic probability.

## Sphinx 4
<!-- TODO: do i really need this? --!>

## Implementation

The pipeline is implemented with a collection of standalone command line tools and a set of bash and python scripts^[The source code is available here: <https://github.com/jonathanewerner/bachelor/tree/master/bin>.].

The tasks are the following, in chronological order:

1. **Preparing the input**

    - The audio file is converted into Sphinx 4 compatible format (16khz, 16bit mono little-endian).
    - A testcase folder with a given shortname (e.g. `psy-15`) is created in the `results`-directory^[<https://github.com/jonathanewerner/bachelor/tree/master/results>] of the source code repository.
    - The reference transcript, the material (PDF format is required) and the converted audio file are moved into a `resources` subfolder of the testcase folder.

2. **Create a material corpus**

    - `pdftohtml -i -xml` is applied on the given material PDF. The XML output representation is input to `pdfreflow`. ^[pdftohtml and pdfreflow are open source linux command line utilities]. Compared to the tool `pdftotext` the combination of these 2 tools preserves paragraphs correctly, whereas `pdftotext` represents each line break in the input pdf as a new paragraph in the output text file. This is a significant disadvantage for the LM creation step, as a newline in the input file there has the semantic "end of sentence" -- so that a sentence split into 4 lines by `pdftotext` would count as 4 sentences in the LM.
    - The HTML output from `pdfreflow` is filtered by taking only relevant HTML-tags such as `<p>`'s (paragraphs) and `<blockquote>`'s, further improving the content-to-noise ratio.
    - The resulting text is then preprocessed for optimal compatibility with the LM creation tool by removing punctuation and superfluous whitespace^[I use a combination of command line text processing (sed) and a perl script from Stephen Marquard here.].
    - The resulting corpus is input to `estimate-ngram`, a LM creation tool from the MIT Language Modeling Toolkit^[<https://code.google.com/p/mitlm/wiki/EstimateNgram>] (MITLMT).

3. **Convert transcript to reference corpus**

    The transcript from Open Yale is supplied as HTML. We apply processing steps to transform it to a corpus ready to be consumed by the WER analysis tool (no punctuation, all lowercase). As these are specific to just the format chosen by Open Yale Courses, the details are omitted, as they have no general use.

4. **Run Sphinx 4 in baseline and interpolated mode**

    `bin/sphinx-interpolated.py` supplies a wrapper around 






















# Analysis

<!--
#. **Methods**

    I will discuss how to analyze the results and develop metrics
    that assess how well the given goals are met with our approach.

    TODO: which metrics follow from the goals of searchability and
    scannability.  define those terms first, discuss what's
    important there ->> keywords!

#. **Analysis**

    I will then perform quantitative analysis on our test dataset
    with the metrics we developed before.

#. **Discussion, Finding and Conclusions**

    I will discuss the findings and draw conclusions from the quantitative analysis concerning the effectiveness of our approach.

--!>



















# References
