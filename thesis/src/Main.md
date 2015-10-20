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
media* (audio- or audiovisual media that mainly consist of spoken
language) doesn't make it possible to scan its contents. You are
"stabbing in the dark" when looking for something specific in a medium
like this and have to consume it like a linear narrative.

This means that although lectures and conference talks are a central
element to science they are much more challenging and tedious to use for
research work.

Being able to a) efficiently search and b) look at the temporal
distribution of important keywords in a visually dense way would
increase the usefulness of speech media in the scientific context
immensely.

One approach to accomplish these goals is to utilize Automatic Speech
Recognition (ASR) in order to transcribe speech to text and also get timing
information for the recognized words. This makes it possible to derive
information about the density of given words at a given point of time in
the talk, which in turn allows to compute word occurence density
maxima. This opens up possibilities for compact visual
representation of the interesting keywords, thus allowing the user to
scan.

The main challenge when using ASR for this task is the recognition
accuracy of technical terms. Most of them are not included in the
language models that are available as these are broad and generic so as
to optimize accuracy over a wide topic spectrum. But when they are
not included in the language model they have a very small chance to be correctly
recognized at all.  <!-- TODO: maybe account for smoothing here? --!>

So the usefulness of applying ASR with a generic language model to the
problem is very small, as the intersection of interesting keywords with
those technical terms that can not be recognized is very big.

The central goal of this thesis is to explore an approach to overcome
this problem. This approach consists of using words from lecture slides
or other notes to generate a lecture-specific language model. This
is then interpolated with a generic language model. Finally the results are compared with the 'baseline'  accuracy of the generic model.

\pagebreak

## Structure of this thesis {-}
The structure of this thesis is as follows:

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
The central research questions I want to investigate in this thesis can
be formulated as follows:

(#) When we apply ASR to university lectures, what is the advantage of using an approach that consists of creating a lecture-specific language model and interpolating it with a generic language model, given that we are interested in improving the recognition accuracy of *interesting keywords* for the sake of
searchability and scannability?

(#) What metric is useful for quantifying this advantage?

A secondary question is: How can we *use* the results from our approach to provide graphical interfaces for improving the user's ability to search and scan the given speech medium?

The exploration of this question will not be at the center of this thesis,
but it will provide practical motivation for the results of our approach.

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

(1) **Dependent vs. independent**. Dependent recognition systems are developed to be used by one speaker, whereas independent systems are developed to be used by *any* speaker of a particular type, i.e North-American speakers. **Adaptive** systems lie between these poles, they are able to adapt to a particular speaker through training.

(2) **Small vs. large vocabulary**. Small vocabularies contain only up to a few hundred words and might be modeled by an explicit grammar, whereas large vocabularies contain tens of thousands of words so as to be able to model general purpose spoken language over a variety of domains.

(3) **Continuous vs. isolated speech**. Isolated speech consists of single words that are spoken with pauses in between them, whereas continuous speech consists of words that are spoken in a connected way. Continuous speech is significantly more difficult to recognize, as it is a) more difficult to find the start and end of words and b) the pronunciation of words changes in relation to their surrounding words.

With these three dimensions we can for example classify the application areas command and control systems, dictation and lecture transcription [@marquard]:

```{.table type="pipe" aligns="LLLL" caption="Three application areas" header="yes"}
Application,                Speaker,     Vocabulary, Duration
Dictation,                  Dependent,   Large,      Connected
Command and control system, Independent, Small,      Isolated
Lecture transcription,      Independent, Large,      Connected
```

The task of automatic lecture transcription can thus be characterized as speaker-independent (SI) large continuous speech recognition (LVCSR).

## Concepts
Speech recognition in the *statistical pattern-recognition approach* paradigm has three major concepts that are necessary for its understanding:

* phonemes and phonetic dictionaries
* acoustic models (AM)
* language models (LM)

### Phonemes
A *phoneme* is "the smallest contrastive linguistic unit which may bring about a change of meaning" [@cruttenden2014gimson, p. 43]. Phonemes are the smallest unit of sound in speech which are combined to form words. The word *sun* for example can be represented by the phonemes `/s/`, `/u/` and `/n/`; the word *table* by `/t/`, `/a/` and `/bl/`.

A language with a specific accent can be described by the set of phonemes that it consists of. Figure \ref{phonemic-chart} uses symbols from the International Phonetic Alphabet (IPA) to display the 44 phonemes that are being used in Received Pronunciation (RP), which is regarded as the "standard accent" in the South of the United Kingdom [@stevenson2011concise].

![Phonemic Chart representing 44 phonemes used in RP British English\label{phonemic-chart}](images/phonemes_50.jpg)

To be able to use phonemes in software an ASCII representation is more suitable. The standard for General American English is the *Arpabet*. Here each phoneme is mapped to one or two capital letters. The digits `0`, `1` and `2` signify stress markers: no stress, primary and secondary stress respectively. A comparison of the IPA format and the arphabet format can be seen in Figure \ref{arpabet}, an excerpt that just shows the *monophthongs* ^[pure vowel sounds with relatively fixed articulation at the start and the end that don't glide towards a new position of articulation].

![Excerpt from the Arpabet @wikiArpabet \label{arpabet}](images/arpabet.png)

### Phonetic dictionaries

Phonetic dictionaries map words to one or more versions of phoneme sequences.

A phonetic representation of a word is specified manually based on the knowledge of how written words *actually sound* when spoken.

An excerpt from the dictionary `cmudict-en-us.dict` @cmuDict looks like this:

    ...
    abdollah AE B D AA L AH
    abdomen AE B D OW M AH N
    abdomen(2) AE B D AH M AH N
    abdominal AE B D AA M AH N AH L
    abdominal(2) AH B D AA M AH N AH L
    ...

The dictionary has 133.425 entries. Generally only words that are in the phonetic dictionary being used can be recognized during speech recognition. *Grapheme^["The smallest unit used in describing the writing system of a language" @florian1996blackwell, p.174]-to-Phoneme converters* (G2P) however make it possible to get phoneme sequence hypotheses for arbitrary words (i.e arbitrary sequences of graphemes). While these results are on average less accurate than manually created variants, they play a vital role in texts with many technical terms as these are often not included in phonetic dictionaries.

### Acoustic models
An acoustic model (AM) describes the relation between an audio signal and the probability that this signal represents a given phoneme.

Acoustic models are created by *training* them on a *corpus* of audio recordings and matching transcripts. When being used in the context of speaker-independent recognition, these models are trained with a variety of speakers that represent a broad spectrum of the language/accent that the acoustic model should represent.

During the *decoding* phase the acoustic model and a phonetic dictionary are used to match sequences of small audio "slices" to possible phonemes and those phonemes to possible word sequence hypotheses. <!-- TODO: oohoo. is this precise? --!>

However, acoustic models alone are not sufficient for speech recognition as they do not have the "higher-level" linguistic information necessary to distinguish e.g. between homonyms and similar-sounding phrases such as "wreck a nice beach" and "recognize speech" [@marquard, 11]. This information is provided by *language models*.

### Language Models

Language models (LM) guide and constrain the search process that a speech recognition system performs by assigning probabilities to sequences of words. They are trained by applying statistical methods on a text corpus. <!-- TODO: mh. awkward --!> Analogous to acoustic models, generic language models use huge text corpora with a broad variety of topics. It is however possible to train language models on small and specialized text corpora, which is the central technical foundation for the approach discussed in this thesis.

The most commonly used form of language models are *n-gram language models*. In the context of a language model an *n-gram* is a sequence of *n* words. 1-grams are called *unigrams*, 2-grams are called *bigrams* and 3-grams are called *trigrams*. An *n-gram language model* maps a set of *n-grams* to probabilities that they occur in a given piece of text.

A key idea in modelling language like this is the *independence assumption*, which says that the probability of a given word is only dependent on the last *n* - 1 words. This assumption significantly decreases the statistical complexity and thus makes it computationally feasible.

N-gram language models do not need to be constrained to one type of n-gram. The *Generic US English Language Model* @cmuLm from CMUSphinx we will use as the baseline for our approach consists of 1-, 2, and 3-grams, for example.

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

While a subfield of ASR called "speaker diarization" tries to account for the interactivity between lecturers and students by identifying multiple speakers, most research treats lectures as single speaker events with the audience as background noise.

Generalization approaches at the language model level try to model common linguistic traits of the lecture genre (this can be called the "macro level"). @kato2000 investigate topic-independent language modeling by creating a large corpus of text from lecture transcripts and panel discussions and then removing topic-specific keywords. ^[In a second step they combine this generalization technique with a specialization technique by adapting the resulting LM with a lecture-specific language model by using preprint papers of a given lecture.]

### Specialization approaches
Specialization approaches try to use context specific to a single lecture ("meso level") or parts of a single lecture ("micro level"^[The three levels are taken from @marquard.]).

Methods used for creating LMs from context information can be categorized into two approaches: direct usage of lecture slides and notes for the creation of LMs versus usage of "derived" data from these materials. Deriving data by using keywords found in slides, using them as web search query terms and using the found documents as the basis for LM creation is explored in @munteanu, @kawahara08 and @marquard.

Using the whole text from lecture slides has been explored by @yamazaki. They compare the *meso level* with the *micro level* by dynamically adapting the LM to the speech corresponding to a particular slide. <!-- TODO: results? --!> @kawahara08 also examine dynamic local slide-by-slide adaption and compare it to global topic adaption using Probabilistic Latent Semantic Analysis (PLSA)^[Latent Semantic Analysis is an approach to document comparison and retrieval which relies on a numeric analysis of word frequency and proximity. <!-- TODO: reformulate --!>] and web text collection, concluding that the latter performs worse then the former because of a worse orientation to topic words. <!-- TODO: find citation that is not from marquard --!>.

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
<!-- TODO: explain how our approach can be classified according to this stuff --!>

## Metrics

<!-- TODO: finish this crap --!>

# Test data { #data }

The test data I will use for evaluating our approach will be from *Open Yale Courses*^[[http://oyc.yale.edu/](http://oyc.yale.edu/)], which is a selection of openly available lectures from Yale university. It consists of 42 courses from 25 departments. Each course has about 20-25 sessions that have an average length of 50 minutes. Each lecture is provided with good quality audio and video recordings, precise manual transcripts and lecture material when available. Only about 20% of the lectures have lecture notes or slides at all and most materials from the natural and formal science departments (physics, astronomics, mathematics) consist of hand-written notes, making them unsuitable for our approach. All talks are in English.

I have chosen the following lectures: (Department, Course, Lecture Number - Title, abbreviation)

- *Biomedical Engineering*: Frontiers of Biomedical Engineering, 1 - What is Biomedical Engineering?  (`biomed-eng-1`)

- *Environmental Studies*: Environmental Politics and Law, 8 - Chemically Dependent Agriculture (`environmental-8`)

- *Geology & Geophysics*: The atmosphere, the ocean, and environmental change, 8 - Horizontal transport (`geology-8`)

- *Philosopy*: Philosophy and the science of human nature, 8 - Flourishing and Detachment (`human-nature-8`)

- *Psychology*: Introduction to Psychology, 14 - What Motivates Us: Sex (`psy-14`)

- *Psychology*: Introduction to Psychology, 5 - What Is It Like to Be a Baby: The Development of Thought (`psy-5`)

The main selection criterion here was topical diversity, the challenge being that the majority of talks with computer-parsable notes was from the humanities.

## Materials overview
The available material is very heterogeneous. I will now give an overview with excerpts which will serve as a basis for examining at a later point if the quality and quantity of the supplied material is correlated with the amount of improvement of our approach.

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
Only about 20% of the courses have lecture material at all; only about 20% of these courses actually have typical "slides" -- the rest provides heterogenous other kinds of material. While it cannot be inferred from this dataset that this is a general condition, it nevertheless shows a clear "real-world" disadvantage of an approach only relying on those materials. We will look at the impact of the varying quality and quantity in the analysis later on.

# The LM-Interpolation approach
I will now describe the LM-Interpolation approach. The high level overview is as follows: we will use the open source speech recognition framework Sphinx 4 ^[Homepage: <http://cmusphinx.sourceforge.net/wiki/sphinx4:webhome>] as the software for performing speech recognition. Sphinx 4 has a modular architecture which allows specifying components of the whole process per configuration. It provides multiple implementations of LMs^[Overview: <http://cmusphinx.sourceforge.net/doc/sphinx4/edu/cmu/sphinx/linguist/language/ngram/LanguageModel.html>], the default one being an n-gram model.

It also provides an `InterpolatedLanguageModel`^[Javadoc: <http://cmusphinx.sourceforge.net/doc/sphinx4/edu/cmu/sphinx/linguist/language/ngram/InterpolatedLanguageModel.html>] (ILM) which allows to specify multiple LMs and weights and interpolate the probabilities for a given n-gram from all models' probabilities ($p = w_1*p_1 + w_2*p_2 + \ldots$ where $w_n$ are the weights ($\sum_{i=1}^n(w_i) = 1$) and $p_i$ is the probability for a given n-gram in $LM_i$).

The purpose of the ILM in our approach is to factor in the importance of keywords. These keywords have to be supplied in the form of an n-gram language model. For this we extract text content from the lecture material, preprocess it and create an n-gram LM from the resulting corpus. Sphinx 4 is then a) run with a generic English n-gram LM only and b) with the ILM configured to use the generic English LM and the keyword language model in a 50/50 weighting. Finally the two resulting transcriptions are compared with a selection of metrics.

As an example, the 1-gram *sex* has a probability of 2.82% in the keyword model of `psy-14`, but a probability of 0.012% in the generic English LM ^[@cmuLm]. When applying 50/50 interpolation, the result is $2.82\%*0.5 + 0.012\%*0.5 = 1.416\%$, which is an increase by the factor ~117 over the generic probability.

## Sphinx 4
<!-- TODO: do I really need this? --!>

## Implementation

The pipeline is implemented with a collection of standalone command line tools and a set of Bash and Python scripts^[The source code is available here: <https://github.com/jonathanewerner/bachelor/tree/master/bin>].

The tasks are the following, in chronological order:

1. **Prepare the input**

    - The audio file is converted into Sphinx 4 compatible format (16khz, 16bit mono little-endian).
    - A testcase folder with a given shortname (e.g. `psy-15`) is created in the `results`-directory^[<https://github.com/jonathanewerner/bachelor/tree/master/results>] of the source code repository.
    - The reference transcript, the material (PDF format is required) and the converted audio file are moved into a `resources` subfolder of the testcase folder.

2. **Create a keyword LM from lecture material**

    - `pdftohtml -i -xml` is applied on the given material PDF. The XML output representation is input to `pdfreflow`^[pdftohtml and pdfreflow are open source linux command line utilities]. Compared to the tool `pdftotext` the combination of these 2 tools preserves paragraphs correctly, whereas `pdftotext` represents each line break in the input PDF as a new paragraph in the output text file. This is a significant disadvantage for the LM creation step, as a newline in the input file there has the semantic "end of sentence" -- so that a sentence split into 4 lines by `pdftotext` would count as 4 sentences in the LM.
    - The HTML output from `pdfreflow` is filtered by taking only relevant HTML-tags such as `<p>`'s (paragraphs) and `<blockquote>`'s, further improving the content-to-noise ratio.
    - The resulting text is then preprocessed for optimal compatibility with the LM creation tool by removing punctuation and superfluous whitespace^[I use a combination of command line text processing (sed) and a perl script from Stephen Marquard here.].
    - The resulting corpus is input to `estimate-ngram`, a LM creation tool from the MIT Language Modeling Toolkit^[<https://code.google.com/p/mitlm/wiki/EstimateNgram>] (MITLMT).

    For clarification intermediate results from this step follow as an example. They are from the test case `psy-5`^["Introduction to Psychology, 5 - What Is It Like to Be a Baby: The Development of Thought"]. Figure \ref{slide} shows an example slide.

    ![Slide from lecture `psy-5` \label{slide}](images/slide_250.png)

    When using `pdftotext` the result looks like this for the given slide:

        Piaget’s Theory of
        Cognitive Development
        • Piaget believed that “children are active
        thinkers, constantly trying to construct more
        advanced understandings of the world”
        • Little scientists
        • These “understandings” are in the form of
        structures he called schemas

    Notice how each newline in the slide maps to a newline in the output. When using the combination of `pdftohtml` and `pdfreflow` the result looks like this:

        <p class="p9">Piaget’s Theory of
        Cognitive Development </p>
        <p class="p10">•  Piaget believed that “children are active
        thinkers, constantly trying to construct more
        advanced understandings of the world” </p>
        <blockquote class="b9">•  Little scientists </blockquote>
        <p class="p10">•  These “understandings” are in the form of
        structures he called <i>schemas</i> </p>

    Notice how a paragraph is captured in a `<p>`-tag. This allows extracting a sentence as one line in the corpus. After applying the preprocessing described above the final corpus for the slide looks like this (where ".. " marks a line continuation):

        piagets theory of cognitive development
        piaget believed that children are active thinkers constantly
        .. trying to construct more advanced understandings of the world
        little scientists
        these understandings are in the form of structures he called schemas


  3. **Convert transcript to reference corpus**

      The transcript from Open Yale is supplied as HTML. We apply processing steps to transform it to a corpus ready to be consumed by the WER analysis tool (no punctuation, all lowercase). As these are specific to just the format chosen by Open Yale Courses, the details are omitted, as they have no general use.

  4. **Run Sphinx 4 in baseline and interpolated mode**

      `bin/sphinx-interpolated.py`^[<https://github.com/jonathanewerner/bachelor/blob/master/bin/sphinx-interpolated.py>] supplies a wrapper for interfacing with Sphinx 4. The Java API of Sphinx 4 is exposed for command line usage by a a JAR package which bundles the Sphinx 4 libraries and a small Main class. This class uses command line arguments supplied from `bin/sphinx-interpolated.py` to correctly configure Sphinx 4 and start the actual recognition.

      Each testcase folder has a configuration file which specifies which models the test run should use:

          {
            "acousticModelPath": "en-new/cmusphinx-en-us-5.2",
            "dictionaryPath": "en-new/cmudict-en-us.dict",

            "languageModelPath": "en-new/cmusphinx-5.0-en-us.lm",
            "keywordModelPath": "model.lm",
            "g2pModelPath": "en-new/en_us_nostress/model.fst.ser",

            "resultsFolder": "biomed-eng-1"
          }

      `bin/sphinx-interpolated.py` interprets the "global" models relative to the repository root-folder `models`, the `resultsFolder` relative to the root folder `results` and the `keywordModelPath` relative to the `resultsFolder`. It then supplies the absolute paths to the JAR. It also supplies absolute output file paths for the transcription result and transcription word timings results.

      This setup ensures reproducible results, as the environment of a given testcase is exactly specified (as long as the same binaries and script versions are assumed).

      `bin/sphinx-interpolated.py` can now be used to run the baseline or/and interpolated version.

5. **Analyze and compare the results**

    Finally the results from the two recognition runs are analyzed and compared by running `bin/hotword-analyze <testcase folder name>`. This performs two things: a) WER comparison and metrics generation and b) keyword visualization.

    5.1 *WER comparison and metrics generation*

    This first calls `bin/wer.py`^[`wer.py` has been adapted from <http://progfruits.blogspot.de/2014/02/word-error-rate-wer-and-word.html>] on each run, which will calculate the WER and show a summary of substituted (SUB), inserted (INS) and deleted (DEL) words when comparing the reference (REF) to the hypothesis (HYP):

        OP  | REF     | HYP
        INS | ****    | this
        INS | ****    | is
        INS | ****    | that
        OK  | this    | this
        OK  | is      | is
        OK  | a       | a
        OK  | course  | course
        SUB | a       | that
        SUB | version | aversion
        OK  | of      | of
        OK  | which   | which
        SUB | i've    | i
        OK  | taught  | taught
        INS | ****    | him
        ...
        ...
        {'Sub': 1230, 'Ins': 674, 'WER': 0.316, 'Del': 324, 'Cor': 5492}

    In a second step it compares the two WER result files with `bin/compare-wer.py`.

    The result is an HTML file with a) shows a WER comparison table and b) various statistical measures which will be explored later. The table (shown in Figure \ref{wer-comparison}) colors correctly recognized words as green and incorrect words as red. It also marks words that have been improved in the interpolated version with a green border and words that have been worsened with a red border.

    ![WER comparison\label{wer-comparison}](images/wer-comparison_150.png)

    5.2 *Keyword visualization*

    Data from the reference and the recognition results is compiled into a format suitable for consumption by a visualisation module, which will be discussed in chapter \ref{viz}.

All intermediate steps from the pipeline are represented as files in the testcase folder. Table \ref{files} gives an overview of the files created by each pipeline step.

```{.table type="pipe" aligns="LLLL" caption="File results of a testcase run\label{files}" header="yes"}
File,                                 Description
**Step 1: Prepare the input**,
`resources/audio.mp3`,                original audio
`resources/audio.wav`,                converted audio
`resources/slides.pdf`,               lecture material
`resources/transcript.html`,          lecture transcript
`config.json`,                        run configuration
 ,
**Step 2: Create a keyword LM**,
`slides.corpus.txt`,                  lecture material corpus
`model.lm`,                           keyword LM

 ,
**Step 3: Convert reference to corpus**,
`reference.corpus.txt`,               reference transcription corpus
`reference_wordcounts.json`,          reference transcription word counts^[They are needed for the visualization later.]

 ,
**Step 4: Run Sphinx 4**,

`sphinx_log_baseline.txt`,            Sphinx 4 logging output
`sphinx_log_interpolated.txt`,
`sphinx_result_baseline.txt`,         Sphinx 4 transcription
`sphinx_result_interpolated.txt`,
`sphinx_word_times_baseline.txt`,     Sphinx 4 word times
`sphinx_word_times_interpolated.txt`,

 ,
**Step 5.1: WER comparison / metrics generation**,
`results.json`,                       run metrics in json format^[This eases parsability for aggregating multiple testcase results later.]
`wer_baseline.txt`,                   WER table / metrics
`wer_interpolated.txt`,
`wer_comparison.html`,                rich WER comparison + metrics

 ,
**Step 5.2: Keyword visualization**,
`cloud_baseline.json`,                data representation for visualization
`cloud_interpolated.json`,

```

# Analysis { #analysis }

I will now discuss how to evaluate the usefulness of the LM-Interpolation approach in light of the goal to improve recognition accuracy of interesting keywords.

## Approaching a good metric
We want to find a metric that describes if and how much the interpolated version improves upon the baseline version. Comparing the generic WER of the two runs does not help to answer the question of how much our approach improves the accuracy of interesting keywords.

### Lecture-scoped WER excluding $top_X$ words

In the interpolated approach we have included the LM created from the lecture material. The basic question to ask when assessing the effectiveness of this approach is: how much better is the WER when *just looking at the words from the lecture material LM*? This is only a starting point however. The lecture material corpus includes a substantial amount of words that would not be classified as "interesting keywords": filler words and very common words. One approach to sort them out is subtracting a set of top $x$ most common words ("$top_X$ words") from this list. The resulting metric can then be parameterized on the given $x$. This is an idea that Marquard uses when he proposes the metric "Ranked Word Correct Rate" (RWCR-n):

> "RWCR-n is defined as the Word Correct Rate for all words in the document which are
not found in the first n words in a given general English word dictionary with words
ranked from most to least frequent." [@marquard, p. 71]

### Lemmas

When searching for a specific term the user is interested in the *lemma* for a given word: when he wants to find occurences of *child* in the given lecture, occurences of "children", "child's", "children's" etc. would also be relevant. This implies two things: 1) when looking at the "atomic" level of improvements and degradations <!-- TODO: worsenings? --!> it is more relevant to have lemmas as atoms and not words and 2) the exact matching (a hypothesis word is only "correct" if it exactly matches the reference word) of the WER algorithm should be "loosened" to also mark hypothesis words as correct if their lemmatized version matches the reference.

The same principle holds for the $top_X$ words: we only want to capture words for which the *lemma* is not in the $top_X$ words.

### Proposed metric: KWER-x

We can distill these concerns into a definition of a metric called *KWER-x*, which expresses the "Keyword Error Rate", where a keyword is defined as the lemma of a word occuring in a given lecture material corpus given that this lemma is not present in the $top_X$ list of most common words of the given language.

The value of x has to be determined empirically: how many of the top words should be filtered out? There has to be a balance between not accidentally excluding keywords (i.e "sex" is in the in the $top_{500}$ words) and filtering out enough filler words. After experimenting with some values I went with $x=500$ for my measurements. It is hard to find a less ad hoc approach to determining the "best" x, as you have no "meta"-metric that assesses how well a given x captures the goal of accurately describing the detection accuracy of keywords; it necessarily is a "best guess". However, while there is no quantitative "meta"-metric, a "qualitative" look at the results obtained is possible.

When looking at results from a run on the `psy-14`-lecture with $x=500$, contrasting the improved^["Improved" means not correctly detected in the baseline version, but detected in the interpolated version.] "normal" words versus the improved keywords, it is obvious that there is a strong density of words that would be actually interesting as keywords, which doesn't hold for the "normal" words, with the exception of a few words like "porn", "machines", "caucasian", "womb", "puzzle" or "social". None of these words however is part of the top 500 words; they just weren't part of the material corpus.

**Normal words improved:** (word, count)

\small{
(and, 17) (to, 13) (are, 10) (the, 9) (that, 7) (a, 7) (in, 6) (is, 5) (you, 5) (face, 5) (from, 4) (but, 4) (over, 3) (find, 3) (for, 3) (of, 3) (or, 3) (with, 3) (an, 3) (different, 3) (them, 2) (around, 2) (not, 2) (like, 2) (large, 2) (some, 2) (out, 2) (we, 2) (about, 2) (there, 2) (than, 2) (this, 2) (have, 2) (it, 2) (how, 2) (effect, 2) (well, 2) (don't, 1) (argued, 1) (interesting, 1) (less, 1) (had, 1) (other, 1) (puzzle, 1) (kick, 1) (do, 1) (food, 1) (big, 1) (they, 1) (advanced, 1) (these, 1) (each, 1) (where, 1) (right, 1) (often, 1) (porn, 1) (year, 1) (our, 1) (machines, 1) (between, 1) (caucasian, 1) (womb, 1) (be, 1) (power, 1) (men, 1) (harvard, 1) (if, 1) (care, 1) (both, 1) (could, 1) (april, 1) (social, 1) (can't, 1) (seems, 1) (into, 1) (one, 1) (done, 1) (likes, 1) (little, 1) (would, 1) (start, 1) (it's, 1) (two, 1) (few, 1) (much, 1) (treat, 1) (lot, 1) (more, 1) (form, 1) (he, 1) (me, 1) (say, 1) (will, 1) (can, 1) (behavior, 1) (many, 1) (my, 1) (mind, 1) (as, 1) (want, 1) (their, 1) (relatively, 1) (huge, 1) (no, 1) (interested, 1) (take, 1) (which, 1) (several, 1) (week, 1) (towards, 1) (again, 1) (firsthand, 1) (who, 1) (such, 1) (largely, 1) (so, 1) (lenses, 1) (keeps, 1) (once, 1) (fact, 1) (that's, 1)
}

\normalsize{}
**Keywords improved**:

\small{
(genes, 9) (coolidge, 5) (sex, 5) (cell, 5) (females, 5) (male, 5) (males, 4) (mate, 4) (differences, 4) (investment, 3) (favorite, 3) (universals, 3) (genetic, 3) (beauty, 3) (choosiness, 3) (attractive, 2) (trivers, 2) (kindness, 2) (polygamous, 2) (answers, 2) (gibbons, 2) (studies, 2) (female, 2) (been, 2) (choose, 2) (gay, 2) (dawkins, 2) (cells, 2) (youth, 2) (deformities, 2) (meaner, 2) (bisexual, 2) (mates, 2) (autism, 2) (average, 2) (exclusive, 1) (evolutionary, 1) (focus, 1) (leads, 1) (skin, 1) (aggression, 1) (looking, 1) (choosy, 1) (factor, 1) (protective, 1) (animal, 1) (choice, 1) (mystery, 1) (evolved, 1) (did, 1) (penguins, 1) (fixed, 1) (conduct, 1) (psychopathy, 1) (intelligence, 1) (culture, 1) (cost, 1) (displays, 1) (sexually, 1) (intact, 1) (sexual, 1) (special, 1) (blue, 1) (reproduce, 1) (woo, 1) (causes, 1) (copulation, 1) (psychologies, 1) (full, 1) (unsure, 1) (theory, 1) (inescapable, 1) (pipefish, 1) (predisposition, 1) (sexes, 1) (surviving, 1) (homosexuality, 1) (known, 1) (television, 1) (unblemished, 1) (science, 1) (empirical, 1) (matter, 1) (beautiful, 1) (tonight, 1) (offspring, 1) (tight, 1) (astrological, 1) (measures, 1) (data, 1) (fertilize, 1) (pernicious, 1) (utero, 1) (contact, 1) (principle, 1) (teeth, 1)}

\normalsize{}

Taking this route of depending on an "ad hoc" value was sufficient to validate our approach because it was possible to manually evaluate the metric performance. Another approach would have been to take the *tf-idf* (Term Frequency - Inverse Document Frequency) as a criterion for "keyword-ness" of words. *tf-idf* computes the "relevance" of a word in the context of a document by taking into account the occurences of the word in the document offset by the word's frequency in a broader corpus. This way common words are rated lower although they occur frequently in the given document. This way there is no need for the arbitrary aspect of choosing an value of $x$ and the negative side effect of accidentally excluding a keyword. On the other hand there would be the need to choose a treshold *tf-idf* score which would have to be met for inclusion into the keyword set.

### Secondary Metrics
The following metrics are evaluated:

- $W$: Number of words
- $KW$: Number of keywords
- $WER_{A|B}$: WER of baseline (A) / interpolated version (B)
- $KWER_{A|B}500$: KWER-500 of baseline (A) / interpolated version (B)
- $W_{worse|improved}$: Proportion of worsened/improved words
- $KW_{worse|improved}$: Proportion of worsened/improved keywords
- $W_{worse|improved}(K)$: Proportion of worsened/improved words that are keywords
- $E$: $W_{improved}(K) - W_{worse}(K)$: A percentage score for "effectiveness" of version B

An example from the lecture `human-nature-8`: The lecture has 5342 words overall, of which 376 are keywords. When looking at the general WER, run A and B both have a score of 43%. This can be "explained" by looking at $W_{worse|improved}$, which is 4% each, meaning that 4% (223/5342) of the words have been improved from run A to B, but 4% (227/5342) them have been worsened, which sums up to 0% difference in WER.

Secondly, the KWER-500 of A is 48% (182/376 keywords) versus 32% for B (121/376 keywords). This improvement of 16% can analogously be explained by looking at $KW_{worse|improved}$: when looking at the 376 keywords, 2% (6/376) of them have been worsened while 18% (67/376) have been improved. $18-2 = 16\%$ explains the improvement from 48% to 32%.

The last metric of $W_{worse|improved}(K)$ looks at the overall worsened/improved words and informs about the proportion of words that were keywords. As mentioned, $W_{worse}$ is 4% (223 of the overall 5342 words have been worsened). What is the proportion of keywords in this number? Analogously, what is the proportion of keywords when looking at the overall improved words? This metric is key in identifying the *effectiveness* (E) of our approach: the $W_{improved}(K)$ value answers the question how well our approach is targeted towards improving the words we are interested in, the $W_{worse}(K)$ value answers the question how big the "side effect" of worsening keywords is. In the example, $W_{worse}(K)$ is 3% (6/227) and $W_{improved}(K)$ is 30% (67/223). This is great: of the 227 overall worsened words only **6** were relevant given our goals. In essence, we can interpret $W_{improved}(K) - W_{worse}(K)$ as an **effectiveness score**, the same way we interpret the difference between $W/KW_{improved}$ and $W/KW_{worse}$ as "singular" metrics (WER and KWER respectively). We can say that our example had an effectiveness of $30-3=27\%$. An effectiveness of 100% would mean that *all* words that were improved had been keywords and *none* of the worsened words would have been keywords.

## Results
The results for the test lectures described above (chapter \ref{data}) are as follows^[Column 2-x represent the lectures, the numbers refer to the following lectures: 1: `human-nature-8`, 2: `environmental-8`, 3: `psy-14`, 4: `psy-5`, 5: `biomed-eng-1`.]:

\small{}
```{.table type="pipe" aligns="MMMMMM" caption="Results" header="yes"}
Metric, 1, 2, 3, 4, 5
W, 5342, 7233, 7618, 7142, 7046
KW, 376, 715, 974, 607, 518
 , , , ,
$WER_A$, 43%, 30%, 34%, 37%, 22%
$WER_B$, 43%, 30%, 34%, 37%, 22%
$W_{improved}$, 4%, 4%, 5%, 5%, 3%
$W_{worse}$, 4%, 4%, 5%, 5%, 3%
$\Delta WER$^[$\Delta$ refers to the improvement from version A to B in this context.], **0%**, **0%**, **0%**, **0%**, **0%**,
 , , , ,
$KWER_A$^[KWER means KWER-500 for brevity if not noted otherwise.], 48%, 34%, 33%, 40%, 32%
$KWER_B$, 32%, 18%, 17%, 19%, 17%
$KW_{improved}$, 18%, 16%, 17%, 22%, 16%
$KW_{worse}$, 2%, 1%, 1%, 0%, 1%
$\Delta KWER$, **16%**, **15%**, **16%**, **22%**, **15%**,
 , , , ,
$W_{improved}(K)$, 30%, 39%, 41%, 40%, 44%
$W_{worse}(K)$, 3%, 2%, 2%, 0%, 2%
E, **27%**, **37%**, **39%**, **40%**, **42%**,

```

\normalsize{}

The mean for $\Delta WER$ is 0.0%, for $\Delta KWER$ it is 16.8%, for E it is 37%.

## Interpretation

Several things are notable. The WER as well as $W_{improved}$ and $W_{worse}$ nearly don't change at all, the differences are only zero-digit absolute amounts. It is interesting that the results are so unambiguous in this respect; it is also unexpected that $W_{improved}$ and $W_{worse}$ always cancel each other out completely.

Assessing the $\Delta KWER$ presents the challenge that no comparison is available that uses the exact same metric. However it is possible to "fuzzily" compare the performance by looking at metrics with the same basic idea.

The metric "RWCR-n" used by @marquard mentioned above is comparable, as it also uses the concept of filtering out the $top_n$ most frequent words; it differs by not taking the lemmatized word version as their atomic unit. With that said, the average improvement in RWCR-10k over 13 lectures also taken from Open Yale Courses is 9.0%, while their average WER decreases by 0.8%.

@kawahara08 use a metric called "Keyword Detection Rate", where keywords are defined as content words (nouns and verbs excluding numbers and pronouns) that appear in the slide text. They then compute the f-measure (the "mean of the recall rate of keywords included in utterances and the precision of keywords detected in ASR results."). They report improvements of 7.5% and 3.0% (for two test sets) in detection rate over the baseline accuracy, while the increase in WER is 2.2% and 1.3% over the baseline respectively^[The mentioned results refer to the combined method of global and local adaptation.].

@miranda do not use a custom metric and report a WER improvement of 3.6%, when interpolating the LM with slide text contents; they achieve an improvement of 5.9% WER when using their proposed method of integrating the speech input with synchronized slide content.

While comparing WER performance has the discussed disadvantage of low relevance to the given evaluation goals and the non-standardized spectrum of custom metrics disallows an objective comparison of the different approaches, it yet gives an impression how our approach's performance relates to other work: the $\Delta KWER$ of 16.8% seems like a good indicator that our approach is a viable solution for the goal of improving speech recognition for searchability and scannability. Additionally, the *effectiveness score* demonstrates that the approach nearly does not worsen keywords at all and 38.8% of the improved words are actually keywords.

In general, the uniform distribution of results over the various topic domains with their very different types of provided materials is also suprising. The results seem to suggest that the form and supposed "quality" of material (e.g. excercise sheet versus lecture slides) does not correlate with the improvement in KWER. The initial assumption that lectures from the natural and formal sciences would be harder to recognize, based on the "naive" presumption that words like "adenosine 5’-triphosphate" would be impossible to recognize, seems to be invalid as well -- apparently the combination of preprocessing, G2P and adapted weighting in the LM makes it possible to detect complicated technical terms like this as well.

### Qualitative Interpretation
While representing the performance of our approach with a set of metrics allows (at least internal) comparability of results, it can not convey a holistic impression of what would actually change for a user of a hypothetic speech media search/scan interface when using data generated with our approach versus the baseline approach.

This impression can be given by looking at the following detailed results of the run on the `biomed-eng-1` lecture.

\small{}
**Normal words improved**

> (of, 8) (that, 7) (the, 6) (or, 6) (and, 5) (a, 5) (in, 4) (to, 4) (is, 4) (it, 3) (course, 3) (into, 2) (an, 2) (your, 2) (from, 2) (than, 2) (one, 2) (those, 2) (this, 2) (talk, 2) (bridge, 1) (set, 1) (don't, 1) (some, 1) (are, 1) (annoying, 1) (really, 1) (again, 1) (there's, 1) (would, 1) (it's, 1) (there, 1) (how, 1) (version, 1) (we're, 1) (which, 1) (you, 1) (more, 1) (week, 1) (be, 1) (students, 1) (free, 1) (i've, 1) (with, 1) (by, 1) (distance, 1) (about, 1) (like, 1) (well, 1) (infectious, 1) (yale, 1) (very, 1) (where, 1) (engineers, 1)

**Normal words worse**:

> (and, 15) (a, 10) (so, 9) (you, 8) (the, 8) (it, 7) (have, 6) (to, 5) (they're, 4) (of, 4) (that, 4) (are, 3) (can, 3) (be, 3) (we, 3) (on, 3) (at, 3) (in, 3) (how, 3) (online, 3) (that's, 3) (day, 2) (we'll, 2) (see, 2) (our, 2) (for, 2) (genes, 2) (could, 2) (it's, 2) (one, 2) (there, 2) (we're, 2) (but, 2) (is, 2) (as, 2) (if, 2) (two, 2) (principle, 2) (concept, 1) (office, 1) (years, 1) (london, 1) (go, 1) (just, 1) (had, 1) (easy, 1) (bridge, 1) (somebody, 1) (increased, 1) (very, 1) (familiar, 1) (safe, 1) (i've, 1) (every, 1) (they, 1) (now, 1) (organ, 1) (did, 1) (doctor's, 1) (because, 1) (old, 1) (some, 1) (really, 1) (what, 1) (said, 1) (lots, 1) (vessels, 1) (health, 1) (approach, 1) (patient, 1) (here, 1) (come, 1) (about, 1) (bow, 1) (or, 1) (cancer, 1) (point, 1) (period, 1) (long, 1) (apply, 1) (city, 1) (would, 1) (leading, 1) (three, 1) (been, 1) (their, 1) (way, 1) (was, 1) (tell, 1) (life, 1) (buy, 1) (posted, 1) (physician, 1) (these, 1) (say, 1) (us, 1) (patient's, 1) (thin, 1) (were, 1) (heart, 1) (an, 1) (heard, 1) (get, 1) (other, 1) (details, 1) (week, 1) (kinds, 1) (i, 1) (mechanical, 1)

**KW improved:**

> (biomedical, 35) (dna, 7) (cells, 7) (engineering, 6) (biochemistry, 3) (cell, 3) (polymer, 2) (graph, 2) (gibbs, 2) (certain, 1) (energy, 1) (site, 1) (occur, 1) (plot, 1) (due, 1) (specifically, 1) (membrane, 1) (answer, 1) (has, 1) (higher, 1) (drugs, 1) (molecule, 1) (known, 1) (post, 1) (polymers, 1) (disease, 1) (order, 1)

**KW worse:**

> (cells, 1) (maintain, 1) (beyond, 1) (genetic, 1) (due, 1)

\normalsize{}

You notice two things: a) the "exchange" of filler words from version A to B and vice versa, which is of no interest for searching and scanning, and b) interesting keywords that have substantial amounts of occurrences, that were not found before, while the amount of worsened KW is tiny. This is the important "qualitative", high-level conclusion: the approach allows users to find technical terms in speech media which they weren't able to find before and it works consistently over a broad spectrum of topics.

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

<!-- TODO:
Relative advantage of IWER/KWER depends on how many of the top words are filtered out.
Advantage decreases with decreasing top X
--!>


# Visualization for Scannability { #viz }

# Improvements

<!-- TODO: IDF as a better metric for relevance? --!>

















# References
