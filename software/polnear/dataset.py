import t4k
import os
import polnear
import csv
import datetime
import corenlp_xml_reader
import brat_reader
import parc_reader
import random


# TODO: provide subset slicing options
CORE_COMPARTMENTS = ['train', 'dev', 'test']
class Dataset(list):

    def __init__(self, *args, **kwargs):

        path = kwargs.pop('path', None)
        path = polnear.SETTINGS.METADATA_PATH if path is None else path
        preload = kwargs.pop('preload', None)

        super(Dataset, self).__init__(*args, **kwargs)

        if preload is not None:
            self.load(preload)
        else:
            self.read_data(path)

    def load(self, article_iterable):
        for article in article_iterable:
            if not isinstance(article, Article):
                raise DatasetError(
                    'Cannot initialize a dataset with non-Article objects')
            self.append(article)

    def read_data(self, path):
        reader = csv.DictReader(open(path),delimiter='\t')
        for row in reader:
            self.append(Article(row))

    def train(self):
        return self.filter(lambda x: x['compartment']=='train')

    def test(self):
        return self.filter(lambda x: x['compartment']=='test')

    def core(self):
        return self.filter(lambda x: x['compartment'] in CORE_COMPARTMENTS)

    def dev(self):
        return self.filter(lambda x: x['compartment']=='dev')

    def parc3_replication(self):
        return self.filter(lambda x: x['compartment']=='parc3-replication')

    def annotator_training(self):
        return self.filter(lambda x: x['compartment']=='annotator-training')

    def filter(self, filter_function):
        return Dataset(preload=filter(filter_function, self))


class ArticleError(Exception):
    pass


class Article(dict):

    LEGAL_FILE_TYPES = {
        'text':'txt',
        'corenlp':'txt.xml',
        'attributions':'ann'
    }

    ARTICLE_METADATA_KEYS = {
        'annotators',
        'author',
        'clinton_count',
        'compartment',
        'credit',
        'filename',
        'level',
        'level_num',
        'publication_date',
        'publication_date_bin',
        'publication_date_str',
        'publisher',
        'stratum',
        'target_entity',
        'title',
        'trump_count',
        'wire'
    }

    DIRECTLY_ASSIGNED_FIELDS = {
        'annotators',
        'author',
        'clinton_count',
        'compartment',
        'credit',
        'filename',
        'publisher',
        'title',
        'wire'
    }

    def __init__(self, article_metadata):
        super(Article, self).__init__()
        self.reset_keys()
        self.map_keys(article_metadata)


    def reset_keys(self):
        for key in self.ARTICLE_METADATA_KEYS:
            self[key] = None


    def map_keys(self, article_metadata):
        self._directly_assign_fields(article_metadata)
        self._level(article_metadata)
        self._annotators(article_metadata)
        self._publication_date(article_metadata)
        self._entity_counts(article_metadata)
        self._stratum(article_metadata)


    def _directly_assign_fields(self, article_metadata):
        for field in self.DIRECTLY_ASSIGNED_FIELDS:
            self[field] = article_metadata[field]


    def _publication_date(self, article_metadata):

        if article_metadata['publication_date'] == '':
            return 

        # First, see if we've got a date string, if not, do nothing
        try:
            publication_date_str = article_metadata['publication_date']
        except KeyError:
            return 

        # Assign the date string, and some derived date representations.
        pub_date = datetime.datetime.strptime(publication_date_str, '%Y-%m-%d')
        self['publication_date'] = pub_date.date()
        self['publication_date_bin'] = get_date_bin(pub_date)
        self['publication_date_str'] = publication_date_str


    def _annotators(self, article_metadata):
        self['annotators'] = article_metadata['annotators'].split('|')


    def _level(self, article_metadata):
        try:
            level_num = int(article_metadata['level'])
            level = 'Level-%d' % level_num
        except ValueError:
            level = article_metadata['level']
            level_num = None
        self['level'] = level
        self['level_num'] = level_num


    def _stratum(self, article_metadata):
        self['stratum'] = (
            self['publisher'],
            self['publication_date_bin'],
            self._get_focal_entity(article_metadata)
        )


    def _entity_counts(self, article_metadata):
        if article_metadata['trump_count'] == '':
            return
        self['trump_count'] = int(article_metadata['trump_count'])
        self['clinton_count'] = int(article_metadata['clinton_count'])
        self['target_entity'] = self._get_focal_entity(article_metadata)


    def _get_focal_entity(self, article_metadata):
        trump_count = article_metadata['trump_count']
        clinton_count = article_metadata['clinton_count']
        if trump_count > clinton_count:
            return 'trump'
        if clinton_count > trump_count:
            return 'clinton'
        else:
            return 'draw'


    def path(self, filetype, annotator=None):

        try:
            extension = self.LEGAL_FILE_TYPES[filetype]
        except KeyError:
            raise ValueError('Unexpected filetype: %s' % filetype)

        dirname = os.path.join(
            polnear.SETTINGS.POLNEAR_DATA_DIR, self['compartment'], filetype)

        if filetype == 'attributions':
            if annotator is None:
                annotator = random.choice(self['annotators'])
            return os.path.join(
                dirname, '%s_%s.%s' % (self['filename'], annotator, extension))
        return os.path.join(dirname, '%s.%s'%(self['filename'], extension))


    def text(self):
        return open(self.path('text')).read()


    def corenlp(self):
        if self.is_parc_or_annotator_training():
            raise ArticleError(
                'Sorry, no corenlp file available for annotator-training files '
                'and parc3-replication files.\n\nTry this instead:\n\n'
                '>>> polnear.data.train()[0].corenlp()'
            )
        return corenlp_xml_reader.AnnotatedText(
            open(self.path('corenlp')).read())


    def attributions(self, annotator=None):
        return brat_reader.BratAnnotatedText(
            open(self.path('attributions', annotator)).read())


    def annotated(self, annotator=None):
        if self.is_parc_or_annotator_training():
            raise ArticleError(
                'Sorry, no corenlp file available for annotator-training files '
                'and parc3-replication files.\n\nTry this instead:\n\n'
                '>>> polnear.data.train()[0].corenlp()'
            )
        return parc_reader.new_reader.ParcCorenlpReader(
            corenlp_path=self.path('corenlp'),
            brat_path=self.path('attributions', annotator)
        )


    def is_parc_or_annotator_training(self):
        return (
            self['compartment'] == 'parc3-replication'
            or self['compartment'] == 'annotator-training'
        )



class DateBinner(object):

    def __init__(self):

        # Monthly bins, offset to start at the 8th of the month, beginning
        # Nov 2015, and ending Nov 2016.
        self._bin_endpoints = [
            datetime.datetime(2015, 11, 8),
            datetime.datetime(2015, 12, 8)
        ] + [datetime.datetime(2016, month, 8) for month in range(1,12)]

    def within_desired_period(self, date):
        if date < self._bin_endpoints[0]:
            return False
        if date >= self._bin_endpoints[-1]:
            return False
        return True

    def get_bin(self, date):
        if not self.within_desired_period(date):
            raise ValueError('Given date is outside desired range.')
        for i, endpoint in enumerate(t4k.skipfirst(self._bin_endpoints)):
            if date < endpoint:
                return i

    def as_date_range_str(self, date_bin):
        start = self._bin_endpoints[date_bin]
        end = self._bin_endpoints[date_bin + 1]
        return '%s - %s' % tuple(d.strftime('%Y/%m/%d') for d in [start, end])



DATE_BINNER = DateBinner()
def within_desired_period(article_metadata):
    return DATE_BINNER.within_desired_period(article_metadata['date'])


def get_date_bin(date):
    return DATE_BINNER.get_bin(date)


