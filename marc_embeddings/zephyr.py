import json, ast
from functools import reduce
from urllib3 import PoolManager
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator


def pick_field(array, name):
    for field in array:
        if name in field:
            return str(field[name])  # TODO: clean this up
        else:
            None


# A Zephyr JSON record composed of field/subfield attributes.
class ZephyrRecord():
    def __init__(self, metadata={}):
        self.metadata = metadata
        self.cid = self.get_field('CID', 'a')

    def get_field(self, field, subfield=None):
        field = pick_field(self.metadata['fields'], field)
        if subfield is None:
            return field
        else:
            field_obj = ast.literal_eval(field)
            return pick_field(field_obj['subfields'], subfield)


# For a selection of MARC fields, transforms every ZephyrRecord into a single DataFrame or a list of strings.
class ZephyrTransformer(BaseEstimator, TransformerMixin):
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


API_HOST = ('http', 'zephir', 'cdlib', 'org')
API_URI = "/api/item/%s.json"
API_URL = ("%s://%s.%s.%s" % API_HOST) + API_URI

http = PoolManager()


def load_from_api(htid):
    response = http.request('GET', API_URL % htid)
    return ZephyrRecord(metadata=json.loads(response.data.decode('utf-8')))
