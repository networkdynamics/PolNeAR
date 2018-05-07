# PolNeAR v.1.0.0 - Political News Attribution Relations Corpus

PolNeAR is a corpus of news articles in which _attributions_ have been
annotated.  An attribution happens when an article cites statements, or
describes the internal state (thoughts, intentions, etc.) of some person or
group.

A common, concrete example of attribution is when someone is directly quoted.

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
See the section entitled "software" at the end of this README for details.

## News Publishers
PolNeAR consists of news articles from 7 US national news publishers \*:

   - Huffington Post        (huff-post)
   - Breitbart              (breitbart)
   - New York Times         (nyt)
   - Politico               (politico)
   - Washington Post        (wash-post)
   - Western Journalism     (west-journal)
   - USA Today              (usa-today)

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

   3. **Majority Candidate**: 504 articles were respectively sampled from
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
and other genres such as editorials, real estate, travel, advice, editorials,
letters, obituaries, reviews, essays, etc.

Articles were classified by genre usign the metadata tags and section
indications  provided by the publisher, either visibly or as hidden attributes
in the html.

It was difficult to find consistent distinguishing markers between hard news
and opinion pieces for some publishers, particularly Huffington Post and
Breitbart.


## Train, Dev, Test splits
PolNeAR is split into training, development, testing subsets.  The analyst
should avoid viewing the dev and test subsets, and should only test a model
architecture once on the test set.


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
other two relate to quality control.  The /data directory also contains a file
called metadata.tsv, which provides a listing of all the news articles along
with metadata, including which annotators have annotated it.

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

Within each of the compartments making up the core dataset--train, dev, and
test--there are three directories, that separately contain the raw article
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


## Quality Control


## Preprocessing


## Manual Annotation
Manual annotation was performed using the BRAT Rapid Annotation Tool, v.1.3. 
Configuration files for the annotation can be found under the brat subfolder.


## Automated Annotation
Automated annotations within directories named "corenlp" were produced by 
running the CoreNLP software [2].

## Accompanying software
If you are a python user, the easiest way to work with this dataset in python
is to install the polnear module, and import it into your programs.

Go to /data/software and do:

    $ python setup.py install

Then, in your python program, import the dataset as follows:

    from polnear import data

The data object behaves like a list.  Each element in the list represents an
article and its acoompanying annotations.  The article is represented as a dict
of metadata attributes, along with a couple helpful methods.

    >>> training_data = data.train()
    >>> training_data[0]
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

You can obtain (read from disk) the raw text, attributions, or corenlp annotations for any article:

    >>> article_full_text = data[0].text()
    >>> annotated_article = data[0].annotated()


[1] _An attribution relations corpus for political news_, 
    Edward Newell, Drew Margolin, Derek Ruths,
    International Conference on Language Resources and Evaluation 2018 
    (LREC 2018).

[2] _The Stanford CoreNLP natural language processing toolkit_,
    Manning, C. D., Surdeanu, M., Bauer, J., Finkel, J., Bethard, S. J., and
    McClosky, D.  Association for Computational Linguistics (ACL) System
    Demonstrations, 2014, pages 55–60.
