import json, ast
from urllib3 import PoolManager
import pandas as pd
from sklearn.base import TransformerMixin

def pick_field(array, name):
    for field in array:
        if name in field:
            return str(field[name])
        else:
            None
                
class ZephyrRecord():
    """A Zephyr JSON record composed of field/subfield attributes.
    """
    def __init__(self, metadata = {}):
        self.metadata = metadata
        self.cid = self.get_field('CID', 'a')

    def get_field(self, field, subfield = None):
        field = pick_field(self.metadata['fields'], field)
        if subfield is None:
            return field
        else:
            field_obj = ast.literal_eval(field)
            return pick_field(field_obj['subfields'], subfield)
        
class ZephyrTransformer(TransformerMixin):
    """Converts a ZephyrRecord into a DataFrame for a selection of MARC fields.
    """
    def __init__(self, selection):
        self.selection = selection
    
    def transform(self, records):
        data = list(map(lambda r: (r.get_field('001'), [r.get_field(f) or '' for f in self.selection]), records))
        return pd.DataFrame.from_items(data, orient = 'index', columns = self.selection)

API_HOST = ('http', 'zephir', 'cdlib', 'org')
API_URI = "/api/item/%s.json"
API_URL = ("%s://%s.%s.%s" % API_HOST) + API_URI

http = PoolManager()

def load_from_api(htid):
    response = http.request('GET', API_URL % htid)
    return ZephyrRecord(metadata = json.loads(response.data.decode('utf-8')))