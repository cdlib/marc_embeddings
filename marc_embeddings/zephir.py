import json
from functools import reduce
from urllib3 import PoolManager
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics.pairwise import cosine_similarity
from marc_embeddings.marc import Field, Subfield


def pick_field(array, name):
    for field in array:
        if name in field:
            return field[name]
        else:
            None


# A Zephir JSON record composed of field/subfield attributes.
class ZephirRecord():
    def __init__(self, metadata={}):
        self.metadata = metadata
        self.cid = self.get_field('CID', 'a')

    def get_field(self, field, subfield=None):
        fields = self.metadata['fields']
        if isinstance(field, Field):
            field_name = field.value
        elif isinstance(field, Subfield):
            field_name = field.parent.value
            subfield = field.value
        else:
            field_name = field

        field_value = pick_field(fields, field_name)

        if not field_value:
            return None
        elif 'subfields' not in field_value:
            return str(field_value)
        elif subfield is None:
            subfields = field_value['subfields']
            return ' '.join([list(s.values())[0] for s in subfields])
        else:
            return pick_field(field_value['subfields'], subfield)


# For a selection of MARC fields, transforms every ZephirRecord into a single DataFrame or a list of strings.
class ZephirTransformer(BaseEstimator, TransformerMixin):
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


API_HOST = ('http', 'd2d-zephir-stg', 'cdlib', 'org')
API_URI = "/api/item/%s.json"
API_URL = ("%s://%s.%s.%s" % API_HOST) + API_URI

http = PoolManager()

import sys

def load_from_api(htid):
    urlstr = API_URL % htid
    sys.stderr.write("GET %s\n" % urlstr)
    sys.stderr.flush()
    response = http.request('GET', urlstr)
    return ZephirRecord(metadata=json.loads(response.data.decode('utf-8')))


# Compares two vectors.
class CosineSimilarity(BaseEstimator, TransformerMixin):
    @staticmethod
    def evaluate(x):
        v_size = int(x.shape[1] / 2)
        v1 = x[:, :v_size]
        v2 = x[:, v_size:]
        return cosine_similarity(v1, v2)[0]

    def transform(self, X):
        return list(map(lambda x: CosineSimilarity.evaluate(x), X))

    def fit(self, *_):
        return self


class SelectField(BaseEstimator, TransformerMixin):
    def __init__(self, field):
        self.index = field

    def transform(self, metadata):
        return list(map(lambda r: r[self.index], metadata))

    def fit(self, *_):
        return self


LEFT = 0
RIGHT = 1


# Operates on a pair of records (as a tuple).
def compare_field(field, vectorizer):
    return Pipeline([
            ('split r1, r2', FeatureUnion([
                ('r1', Pipeline([
                    ('select r1', SelectField(LEFT)),
                    ('get field', ZephirTransformer([field])),
                    ('flatten', FlattenTransformer()),
                    ('vectorize', vectorizer)
                ])),
                ('r2', Pipeline([
                    ('select r2', SelectField(RIGHT)),
                    ('get field', ZephirTransformer([field])),
                    ('flatten', FlattenTransformer()),
                    ('vectorize', vectorizer)
                ]))
            ])),
            ('cosine similarity', CosineSimilarity())
        ])
