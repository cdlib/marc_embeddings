import xmltodict
from functools import reduce
from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd
import re


RECORD_START = '^<record>'
RECORD_END = '</record>$'

def load_from_xml(filename):
    with open(filename) as f:
        record = ""
        in_record = False
        for line in f:
            if re.match(RECORD_START, line):
                in_record = True
            if in_record:
                record += line
            if re.match(RECORD_END, line):
                in_record = False
                doc = xmltodict.parse(record)
                record = ""
                yield LCRecord(metadata = doc['record'])

        #doc = xmltodict.parse(f.read())
        #for r in doc['collection']['record']:
        #    yield LCRecord(metadata=r)


def pick_field(fields, name):
    for field in fields:
        if field['@tag'] == name:
            return field
    None


def pick_subfield(subfields, name):
    if type(subfields) == list:
        for subfield in subfields:
            if subfield['@code'] == name:
                return subfield['#text']
    else:
        if subfields['@code'] == name:
            return subfields['#text']
    None


class LCRecord():
    def __init__(self, metadata={}):
        self.metadata = metadata

    def get_field(self, field, subfield=None):
        field = pick_field(self.metadata['datafield'], field) or pick_field(self.metadata['controlfield'], field)
        if field is None:
            return None
        if subfield is None:
            return str(field)  # TODO: clean this up
        else:
            if 'subfield' in field:
                return str(pick_subfield(field['subfield'], subfield))  # TODO: clean this up
            else:
                return None


# For a selection of MARC fields, transforms every LOCRecord into a single DataFrame or a list of strings.
class LCTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, selection, dataframe=False):
        self.selection = selection
        self.use_dataframe = dataframe

    def fit(self, *_):
        return self

    def transform(self, records):
        data = list(map(lambda r: (r.get_field('001'), [r.get_field(f) or '' for f in self.selection]), records))
        if self.use_dataframe:
            return pd.DataFrame.from_items(data, orient='index', columns=self.selection)
        else:
            return [d[1] for d in data]


# Transforms a list of lists of values into a list of values.
class FlattenTransformer(BaseEstimator, TransformerMixin):
    def fit(self, *_):
        return self

    def transform(self, records):
        return list(reduce(lambda a, b: a + b, records))
