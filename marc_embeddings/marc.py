from .frbr import Entity
from enum import Enum
import collections


class Field:
    def __init__(self, value, level=Entity.WORK, subfields=[]):
        self.value = value
        self.level = level
        self.subfields = subfields


class Subfield:
    def __init__(self, value, level=None):
        self.value = value
        self.level = level


class MainEntry(Enum):
    PERSONAL_NAME = Field('100', subfields=[])
    CORPORATE_NAME = Field('110', subfields=[])
    MEETING_NAME = Field('110', subfields=[])
    UNIFORM_TITLE = Field('130', subfields=[])


class TitleRelated(Enum):
    ABBREVIATED_TITLE = Field('210', subfields=[])
    KEY_TITLE = Field('222', subfields=[])
    UNIFORM_TITLE = Field('240', subfields=[
        Subfield('a', Entity.WORK),
        Subfield('d', Entity.WORK),
        Subfield('f', Entity.WORK),
        Subfield('g'),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('k', Entity.WORK),
        Subfield('l', Entity.EXPRESSION),
        Subfield('m', Entity.WORK),
        Subfield('n', Entity.WORK),
        Subfield('o', Entity.EXPRESSION),
        Subfield('p', Entity.WORK),
        Subfield('r', Entity.WORK),
        Subfield('s', Entity.WORK)
    ])
    TRANSLATION_OF_TITLE_BY_CATALOGING_AGENCY = Field('242', subfields=[])
    COLLECTIVE_UNIFORM_TITLE = Field('243', subfields=[])
    TITLE_STATEMENT = Field('245', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('b'),
        Subfield('c', Entity.MANIFESTATION),
        Subfield('f', Entity.WORK),
        Subfield('g', Entity.WORK),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('k', Entity.WORK),
        Subfield('n', Entity.MANIFESTATION),
        Subfield('p', Entity.MANIFESTATION),
        Subfield('s', Entity.EXPRESSION)
    ])
    VARYING_FORM_OF_TITLE = Field('246', subfields=[])
    FORMER_TITLE = Field('247', subfields=[])


class EditionImprint(Enum):
    EDITION_STATEMENT = Field('250', subfields=[])
    MUSICAL_PRESENTATION_STATEMENT = Field('254', subfields=[])
    CARTOGRAPHIC_MATHEMATICAL_DATA = Field('255', subfields=[])
    COMPUTER_FILE_CHARACTERISTICS = Field('256', subfields=[])
    COUNTRY_OF_PRODUCING_ENTITY = Field('257', subfields=[])
    PHILATELIC_ISSUE_DATA = Field('258', subfields=[])
    PUBLICATION_DISTRIBUTION_IMPRINT = Field('260', subfields=[])
    PROJECTED_PUBLICATION_DATE = Field('263', subfields=[])
    PRODUCTION_PUBLICATION_DISTRIBUTION_MANUFACTURE_COPYRIGHT_NOTICE = Field('264', subfields=[])
    ADDRESS = Field('270', subfields=[])


class AllFields(Enum):
    MAIN_ENTRY = MainEntry
    TITLE_RELATED = TitleRelated
    EDITION_IMPRINT = EditionImprint


def flatten(*args):
    """Flatten an object containing MARC fields.
    """
    for arg in args:
        if type(arg) in [MainEntry, TitleRelated, EditionImprint]:
            yield arg.value.value
        elif type(arg) == list:
            for v in arg:
                yield from flatten(v)
        elif type(arg) == str:
            yield arg
        elif isinstance(arg, collections.Iterable):
            for v in arg:
                yield from flatten(v.value)
        elif type(arg) == dict:
            for v in arg.values():
                yield from flatten(v)
        elif isinstance(arg, Field):
            yield arg.value
        else:
            pass


def select(*args):
    """Produce a list of all MARC fields.
    """
    return sorted(list(set(flatten(*args))))
