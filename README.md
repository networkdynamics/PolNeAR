# PolNeAR v.1.0.0 - Political News Attribution Relations Corpus

PolNeAR is a corpus of news articles in which _attributions_ have been
annotated.  An attribution occurrs when an article cites statements, or
describes the internal state (thoughts, intentions, etc.) of some person or
group.  A direct verbatim quote is an example of attribution, as is the paraphrasing of a source's intentions or beliefs.

## Benefits
In 2018, PolNeAR is the largest attribution dataset by total number of
annotated attribution relations.  It is also, based on analysis described in
[1], the most _complete_ attribution corpus, in the sense of having high
pseudo-recall.  

PolNeAR annotations are univocal, meaning that each token in the articles has
just one label (source, cue, content, or none), and that each token is involved
in at most one attribution.  For modelling purposes, this means that a PolNeAR
annotation is a tag sequence.

## Bonus software for Python users

This repository contains the full PolNeAR dataset, along with some software to
make it easier to work with the data in Python, in case you are a Python user.
See the section entitled "Accompanying software" at the end of this README for
details.

## News Publishers
PolNeAR consists of news articles from 7 US national news publishers \*:

   - Huffington Post        (`huff-post`)
   - Breitbart              (`breitbart`)
   - New York Times         (`nyt`)
   - Politico               (`politico`)
   - Washington Post        (`wash-post`)
   - Western Journalism     (`west-journal`)
   - USA Today              (`usa-today`)

\* Publisher codes used in metadata shown in brackets.

## News Coverage and Sampling

The articles in PolNeAR come from the coverage, by 7 US national news
publishers, of the campaigns in the US General Election on 8 Nov 2016.

Only articles that mention at least one of the candidates, Donald Trump or 
Hillary Clinton are included.

Stratified sampling was used to draw articles uniformly from time period,
publisher, and candidate of focus in the article, as follows.

   1. **Publisher**: 144 articles were sampled from each publisher.

   2. **Time**: 84 articles were sampled uniformly from each 12 month-long
      period between 8-Nov-2015 to 8-Nov-2016.

   3. **Focal Candidate**: 504 articles were respectively sampled from
      articles mentioning Trump or Clinton the weak majority of the time.  A
      candidate is mentioned the weak majority of the time if it is mentioned at
      least as many times as its opponent.

A stratum consists of a triple (publisher, time-bucket, focal-candidate).
In this dataset, there are:

    7 publishers * 12 time-periods * 2 focal-candidates = 168 strata

Each stratum contributes 6 randomly-sampled articles to the dataset, for a
total of 1008 articles.


## Genre
We endeavored to include only the hard news genre, and to exclude soft news,
and other genres such as editorials, real estate, travel, advice, letters,
obituaries, reviews, essays, etc.

Articles were classified by genre usign the metadata tags and section
indications  provided by the publisher, either visibly or as hidden attributes
in the html.

It was difficult to find consistent distinguishing markers between hard news
and opinion pieces for some publishers, particularly Huffington Post and
Breitbart.


## Train, Dev, Test splits
PolNeAR is split into training, development, testing subsets.  The analyst
should avoid viewing the dev and test subsets, and should only test a model
architecture once on the test set.  The train subset includes all articles from
the first 10 month-long periods of coverage.  The dev and test subsets include
respectively articles drawn from the 11th and 12th month.


## Statistics
<pre>
==========================================================
 &#35 Articles, core dataset         |  1008    |  
 &#35 Articles, annotator training   |     4    |  
 &#35 Articles, PARC3 replication    |    54    |  
 &#35 Publishers                     |     7    |  
 &#35 Words                          |   760    |  thousand
 &#35 Attributions                   |    24    |  thousand
 Token-wise Krippendorff's alpha  |    75.4  |     %
 Attribution-wise agreement (agr) |    92.3  |     %
 Pseudo-recall of PARC3           |    94.2  |     %
 &#35 False negatives estimated\*    |  1060    |  
==========================================================
* Estimated from pseudo-recall on PARC3 articles, extrapolated to the size of
the corpus
</pre>


## Data File Structure

The PolNeAR data resides under the /data directory.  There is one subdirectory
for each _compartment_ of the dataset.  There are 5 compartments.  Three of the
compartments correspond to the core dataset's train/test/dev subsets.  The
other two relate to quality control during annotation.  The /data directory
also contains a file called metadata.tsv, which provides a listing of all the
news articles along with metadata, including which annotators have annotated
it.

<pre>
- /data
    │
    │  // Core Dataset
    ├─ train
    ├─ dev
    ├─ test
    │
    │  // Quality Control
    ├─ parc3-replication
    ├─ annotator-training
    │
    │  // Table of contents and metadata
    └─ metadata.tsv
</pre>

Within each of the compartments making up the core dataset&mdash;train, dev, and
test&mdash;there are three directories, that separately contain the raw article
text, attribution annotations in standoff format, and CoreNLP annotations in
xml format.  The training compartment is shown as an example:

<pre>
- /data
   ├─ train
   │   ├─ text
   │   ├─ attributions
   │   └─ corenlp
  ...
</pre>

The contents of the parc3-replication and annotator-training compartments are
similar, but lack CoreNLP annotations.  The parc3-replication also lacks the
original text files, which should be obtained from the Penn Treebank 2 corpus.

<pre>
- /data
    ├─ parc3-replication
    │   └─ attributions
    │
    ├─ annotator-training
    │   ├─ text
    │   └─ attributions
   ...
</pre>


## Preprocessing

## Annotation
The annotation of attributions was performed manually by 6 trained annotators,
who each annotated approximately 168 articles in the core dataset, 4 articles
for assessing training, and 54 articles for comparison to PARC3.

To provide core NLP annotations, such as tokenization, sentnece splitting,
part-of-speech tagging, constituency and dependency parsing,  named entity
recognition, and coreference resolution, we provide annotations produced automatically by the CoreNLP software in parallel to the manual attribution annotations.  See _Automated Annotation by CoreNLP_ below.

## Manual Annotation
### Training
All annotators were trained in two 2-hour periods, in which they reviewed the
the guidelines (see /annotation-guidelines/guidelines.pdf).  after each major
section in the guidelines, we conducted a group discussion amongst the
annotators to answer any questions and rectify any misconceptions.  Annotators
were provided practice 2 practice articles as practice annotation.  

Annotators were then provided the templates document
(/annotation-guidelines/templates.pdf), which was designed to provide quick
reference and examples to guide annotation.

After annotating the practice articles, we discussed the annotations as a
group, using the existing language in the guidelines to resolve disagreements
or misconceptions.

Near the end of the second training session, annotators were shown examples in 
/annotation-guidelines/guidelines-training-interactive.pdf, and asked to 
describe how they would annotate it.  The examples were designed to be
difficult, but to have a correct answer according to the guidelines.

### Training Articles
After training was complete, annotators annotated 4 articles, to measure their initial agreement and verify that training had been successful.  These articles provide an indication of agreement level for annotators immediately after the training process.

### Ongoing Monitoring of Annotation Quality
Each annotator annotated approximately 18 articles every week.  As a quality
control measure, weekly group meetings were held with all annotators in which
which we reviewed two articles that had been annotated by all annotators.
During the meeting, the annotations that each annotator made in the two shared
articles were aligned to clearly show the cases where annotators had agreed or
disagreed on how to perform the annotation.  The discussions were conducted to
encourage consensus by appealing to the existing guidelines and, especially,
the templates. 

## Automated Annotation by CoreNLP
Automated annotations within directories named "corenlp" were produced by 
running the CoreNLP software [2], using the following annotators: `tokenize`,
`ssplit`, `pos`, `lemma`, `ner`, `parse`, and `dcoref`; and with the output
format 'xml' chosen.  The following was set in the properties file:

    ner.model = 'edu/stanford/nlp/models/ner/english.conll.4class.distsim.crf.ser.gz'

## Annotation Quality
The quality of annotations was assessed using various agreement-based metrics.
Please see the associated paper for results [1].

## Article Metadata

The file `PolNeAR/data/metadat.tsv` lists every article in PolNeAR and provides
several metadata fields containing information about the article itself, and how it was annotated. 

### Metadata about the articles
The following fields are hopefully self-explanatory:
`filename`, `publisher`, `publication_date`, `author`, `title`, 

The fields `trump_count` and `clinton_count` indicate the number of times
respectively that Donald Trump and Hillary Clinton, the presidential
candidates, were mentioned.  Care was taken using regexes to disambiguate such
mentions from others, such as Donald Trump Jr. or Bill Clinton.

The fields `credit` and `wire` are used respectively to indicate when the
publisher has given credit for a story to another news publisher, or to a
wire service, such as AP or Reuters.

### Metadata about annotation
The fields `compartment`, `level`, and `annotators` indicate how the article was subjected to annotation.  First, `compartment` indicates the compartment into which the annotation falls: 
 - `annotator-training` indicates that the articles were used to during
   training of the annotators, to test their interannotator agreement and
   verify annotations against an expert application of the annotation
   guidelines.
 - The `train`, `dev` and `test` compartments make up the core dataset that
   should normally be used.  The `test` compartment should never be viewed
   directly, but only used to calculate model evaluation statistics.
 - The `parc-replication` compartment contains files sampled from the PARC3
   dataset, and used to compare its annotation process to that of PolNear.

Next, the `annotators` field is a pipe-separated list of unique IDs for the
annotators that annotated the specific article.  Most articles are only
annotated by one annotator, but those used to test agreement are annotated by
many annotators.

Finally, the `level` field indicates the sequential annotation batch in which
the article was annotated.  Annotators proceeded through the datset in a series
of batches, as follows:

 - Level-0\*
 - Level-1
 - ...
 - Level-4
 - PARC-1A and PARC-1B
 - PARC-2A and PARC-2B
 - Level-5
 - Level-6
 - ...
 - Level-23

\* Along with the 34 PARC3 articles in the PARC-X levels, 20 PARC3 articles
were interspersed into Level-0 to provide an early check for agreement with the
PARC3 approach to annotation.


## Accompanying software
If you are a Python user, the easiest way to work with this dataset in Python
is to install the polnear module, and import it into your programs.

Go to /data/software and do:

    $ python setup.py install

Then, in your Python program, import the dataset as follows:

    from polnear import data

The `data` object behaves like a `list`.  Each element in `data` is an
`Article` object, representing one PolNeAR article its acompanying annotations.
The `Article` object is `dict`-like, and is populated with the metadata for the
article it represents.

	>>> data[0]
    {'annotators': ['4b22', '4e07', '5fec', '6b86', 'd473', 'ef2d'],
     'author': 'Chris Tomlinson',
     'clinton_count': 0,
     'compartment': 'annotator-training',
     'credit': 'None',
     'filename': 'breitbart_2016-03-11_activists-brick-up-entrance-to-m',
     'level': 'None',
     'level_num': None,
     'publication_date': datetime.date(2016, 3, 11),
     'publication_date_bin': 4,
     'publication_date_str': '2016-03-11',
     'publisher': 'breitbart',
     'stratum': ('breitbart', 4, 'draw'),
     'target_entity': 'draw',
     'title': 'Activists Brick Up Entrance To Migrants-Only Polling Station Ahead Of Weekend Elections',
     'trump_count': 0,
     'wire': 'None'}

As you can see above, the metadata provided matches that contained in metadata.tsv, with the following modifications and additions:
 - `level_num`: indicates the annotation batch as an integer.  `level_num` is
   only non-`None` for articles that are part of the core dataset (i.e. the
   `train`, `dev`, and `test` compartments).
 - `target_entity`:  The candidate, `trump` or `clinton`, that was mentioned
   the most times, or `draw`.
 - `publication_date`: a `datetime.date` object representing the publication
   date.
 - `publication_date_str`: A `YYYY-mm-dd`-formatted `str` representation of the
   date.
 - `publication_date_bin`: The index of the month-long temporal stratum from
   which the article was sampled.  (The 1-year period was divided into 12 equal
   month-long strata that do not correspond to the beginnings of months.)
 - `stratum`: A triple that identifies the fully-specified stratum from which
   this article was sampled, having the format `(publisher,
   publication_date_bin, target_entity)`.

Looking closely at the `Article` object above, we see that it is from the
`'annotator-training'` compartment.  That's because, by default, the `data`
object lists *all* articles in the PolNeAR dataset, including those used to test
annotator trainin and those used to compare PolNeAR annotations to PARC3
annotations.  

But usually, we want to access the core dataset, which is split into train,
dev, and test subsets:

	>>> train = data.train()
	>>> dev = data.dev()
	>>> test = data.test()

If, for some reason, you want to work with the articles used to replicate PARC3, or to work with the articles used to assess annotator training, you can:

	>>> annotator_training = data.annotator_training()
	>>> parc3_replication = data.parc3_replication()

These objects, `train`, `dev`, `test`, `annotator_training`, and
`parc3_replication`, are like the original `data` object, in that they are
`list`-like and provide a list of `Article` objects, except that they are
restricted to the desired subset of PolNeAR.

Now, let's focus on `Article` objects.  In addition to containing all of the
article's metadata, they allow you to easily access the raw text and
annotations associated to that article. For example you can get the raw text of
an article as a `unicode`:

    >>> article = train[0]
    >>> article_text = article.text()

More interestingly, you can get a representation of the article with
annotations:

    >>> article_annotated = data[0].annotated()

Here, `article_annotated` is an `AnnotatedText` object which is modelled
after the `corenlp_xml_reader.AnnotatedText` object.  It
allows you to easily iterate over sentences, tokens, or attributions, and to
access syntax annotations like POS tags, constituency parse, dependency parse,
and coreference annotations.  Most of this functionality is already documented
in `corenlp_xml_reader`, so please refer to [its
documentation](http://corenlp-xml-reader.readthedocs.io/en/latest/).  Here, we
document the access of attribution annotations.

First, let's suppose you want to annotate over the sentences of a document,
and then do something every time you encounter an attribution.

	>>> for sentence in article_annotated.sentences:
	...     for attribution_id in sentence['attributions']:
    ...         print attribution_id
    set([])
    set(['E1'])
    set(['E1'])
    set(['E2'])
    set([])
    set(['E3'])
    set([])
    set(['E4'])
	... [truncated]

As you can see, the `'attributions'` key of the `sentence` objects is a set
that contains all the attribution IDs for attributions that involve tokens from
that sentence.  Usually a sentence participates in zero or one attribution, but
sometimes multiple attributions occur in one sentence.

Of course, here, we just printed attribution IDs.  To get ahold of the
attribution object, which contains information about the source, cue and
content spans, look it up in the documnet's dictionary of attributions:

	>>> article_annotated.attributions['E1']
    {'content': [11: the (120,123) DT -,
      12: presidential (124,136) JJ -,
      13: ambitions (137,146) NNS -,
      14: of (147,149) IN -,
      15: three (150,155) CD NUMBER,
      16: Republican (156,166) JJ MISC,
      17: hopefuls (167,175) NNS -,
      18: : (175,176) : -,
      19: Jeb (177,180) NNP -,
      20: ! (180,181) . -,
       0: , (181,182) , -,
       1: Ben (183,186) NNP PERSON,
       2: Carson (187,193) NNP PERSON,
       3: , (193,194) , -,
       4: and (195,198) CC -,
       5: Donald (199,205) NNP PERSON,
       6: Trump (206,211) NNP PERSON],
     'cue': [10: mocked (113,119) VBD -],
     'id': 'E1',
     'source': [ 9: we (110,112) PRP -]}

Attributions are themselves `dict`-like.  They include the keys `source`,
`cue`, and `content`, each of which is a list of the tokens that take part in
the respective source, cue, and content spans.

The attribution objects also know which sentences they are involved in, so if you have an attribution, you can easily get the implicated sentences:

	>>> print article_annotated.attributions['E1'].get_sentence_ids()
	set([1, 2])

This shows that the attribution `'E1'` is found in sentences 1 and 2 (due to
zero indexing, these are the second and third sentences in the document).

Another way to access attribution information is on tokens themselves.  If you
iterate over the tokens of the document or a particular sentence, you can check
whether that token plays a role in an attribution.  Recall that, in the
`AttributedText` object, `token`s are `dict`-like.  The `'attributions'` key
provides a dictionary that indicates what role the token plays in any
attributions.  We already know that sentence `1` has an attribution in it, so
let's use it as an example:


	>>> for token in annotated_text.sentences[1]['tokens']:
			print token['attributions']
	{}
	{}
	{}
	{}
	{}
	{}
	{}
	{}
	{}
	{'E1': set(['source'])}
	{'E1': set(['cue'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}
	{'E1': set(['content'])}

As you can see, `token['attributions']` is a dictionary, with the attribution
ID as keys, and a set of roles that the token plays in that attribution.
Although in PolNeAR a given token can only play a single role in a single
attribution, in PARC3, tokens can play multiple roles (e.g. be both part of the
source and cue) and can partipate in multiple attributions (e.g. in the case of
nested attributions).

So in all, there are three ways to access attribution information:

 1. Iterate over the values of the `annotated_document.attributions` dictionary,
 2. Starting from a sentence, look to the value of `sentence['attributions']`,
 3. Starting from a token, look to the value of `token['attributions']`.

Again, for more information on how to navigate the AnnotatedText object and access other annotations such as coreference resolution, dependency and constituency parses, etc., refer to documentation for [`corenlp_xml_reader.AnnotatedText`](http://corenlp-xml-reader.readthedocs.io/en/latest/).


[1] _An attribution relations corpus for political news_, 
    Edward Newell, Drew Margolin, Derek Ruths,
    International Conference on Language Resources and Evaluation 2018 
    (LREC 2018).

[2] _The Stanford CoreNLP natural language processing toolkit_,
    Manning, C. D., Surdeanu, M., Bauer, J., Finkel, J., Bethard, S. J., and
    McClosky, D.  Association for Computational Linguistics (ACL) System
    Demonstrations, 2014, pages 55–60.
