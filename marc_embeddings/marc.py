from .frbr import Entity
from enum import Enum
import collections


"""
See http://www.loc.gov/marc/marc-functional-analysis/functional-analysis.html

This data model works with a restricted set of entities relevant to machine
feature extraction. Control numbers are not modeled. Referred entities are not
modeled.
"""


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
    PERSONAL_NAME = Field('100', subfields=[
        Subfield('a', Entity.PERSON),
        Subfield('b', Entity.PERSON),
        Subfield('c', Entity.PERSON),
        Subfield('d', Entity.PERSON),
        Subfield('f', Entity.WORK),
        Subfield('j', Entity.PERSON),
        Subfield('k', Entity.WORK),
        Subfield('l', Entity.EXPRESSION),
        Subfield('n', Entity.WORK),
        Subfield('p', Entity.WORK),
        Subfield('q', Entity.PERSON),
        Subfield('t', Entity.WORK)
    ])
    CORPORATE_NAME = Field('110', subfields=[
        Subfield('a', Entity.CORPORATE_BODY),
        Subfield('b', Entity.CORPORATE_BODY),
        Subfield('c', Entity.CORPORATE_BODY),
        Subfield('d', Entity.CORPORATE_BODY),
        Subfield('f', Entity.WORK),
        Subfield('k', Entity.WORK),
        Subfield('l', Entity.EXPRESSION),
        Subfield('n', Entity.WORK),
        Subfield('p', Entity.WORK),
        Subfield('t', Entity.WORK)
    ])
    MEETING_NAME = Field('111', subfields=[
        Subfield('a', Entity.CORPORATE_BODY),
        Subfield('c', Entity.CORPORATE_BODY),
        Subfield('d', Entity.CORPORATE_BODY),
        Subfield('e', Entity.CORPORATE_BODY),
        Subfield('f', Entity.WORK),
        Subfield('k', Entity.WORK),
        Subfield('l', Entity.EXPRESSION),
        Subfield('n', Entity.WORK),
        Subfield('p', Entity.WORK),
        Subfield('q', Entity.CORPORATE_BODY),
        Subfield('t', Entity.WORK)
    ])
    UNIFORM_TITLE = Field('130', subfields=[
        Subfield('a', Entity.WORK),
        Subfield('d', Entity.WORK),
        Subfield('f', Entity.WORK),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('k', Entity.WORK),
        Subfield('l', Entity.EXPRESSION),
        Subfield('m', Entity.WORK),
        Subfield('n', Entity.WORK),
        Subfield('o', Entity.EXPRESSION),
        Subfield('p', Entity.WORK),
        Subfield('r', Entity.WORK),
        Subfield('s', Entity.WORK),
        Subfield('t', Entity.WORK)
    ])


class TitleRelated(Enum):
    ABBREVIATED_TITLE = Field('210', subfields=[
        Subfield('a', Entity.MANIFESTATION)
    ])
    KEY_TITLE = Field('222', subfields=[
        Subfield('a', Entity.MANIFESTATION)
    ])
    UNIFORM_TITLE = Field('240', subfields=[
        Subfield('a', Entity.WORK),
        Subfield('d', Entity.WORK),
        Subfield('f', Entity.WORK),
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
    TRANSLATION_OF_TITLE_BY_CATALOGING_AGENCY = Field('242', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('c', Entity.MANIFESTATION),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('n', Entity.MANIFESTATION),
        Subfield('p', Entity.MANIFESTATION)
    ])
    COLLECTIVE_UNIFORM_TITLE = Field('243', subfields=[
        Subfield('a', Entity.WORK),
        Subfield('d', Entity.WORK),
        Subfield('f', Entity.WORK),
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
    TITLE_STATEMENT = Field('245', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('c', Entity.MANIFESTATION),
        Subfield('f', Entity.WORK),
        Subfield('g', Entity.WORK),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('k', Entity.WORK),
        Subfield('n', Entity.MANIFESTATION),
        Subfield('p', Entity.MANIFESTATION),
        Subfield('s', Entity.EXPRESSION)
    ])
    VARYING_FORM_OF_TITLE = Field('246', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('n', Entity.MANIFESTATION),
        Subfield('p', Entity.MANIFESTATION)
    ])
    FORMER_TITLE = Field('247', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('n', Entity.MANIFESTATION),
        Subfield('p', Entity.MANIFESTATION),
        Subfield('x', Entity.MANIFESTATION)
    ])


class EditionImprint(Enum):
    EDITION_STATEMENT = Field('250', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('b', Entity.MANIFESTATION)
    ])
    MUSICAL_PRESENTATION_STATEMENT = Field('254', subfields=[
        Subfield('a', Entity.EXPRESSION)
    ])
    CARTOGRAPHIC_MATHEMATICAL_DATA = Field('255', subfields=[
        Subfield('a', Entity.EXPRESSION),
        Subfield('b', Entity.EXPRESSION),
        Subfield('c', Entity.WORK),
        Subfield('d', Entity.WORK),
        Subfield('e', Entity.WORK),
        Subfield('f', Entity.WORK),
        Subfield('g', Entity.WORK)
    ])
    COMPUTER_FILE_CHARACTERISTICS = Field('256', subfields=[
        Subfield('a', Entity.EXPRESSION)
    ])
    COUNTRY_OF_PRODUCING_ENTITY = Field('257', subfields=[
        Subfield('a', Entity.EXPRESSION)
    ])
    PUBLICATION_DISTRIBUTION_IMPRINT = Field('260', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('b', Entity.MANIFESTATION),
        Subfield('c', Entity.MANIFESTATION),
        Subfield('e', Entity.MANIFESTATION),
        Subfield('f', Entity.MANIFESTATION),
        Subfield('g', Entity.MANIFESTATION),
        Subfield('3', Entity.MANIFESTATION)
    ])
    PROJECTED_PUBLICATION_DATE = Field('263', subfields=[
        Subfield('a', Entity.MANIFESTATION)
    ])
    ADDRESS = Field('270', subfields=[
        Subfield('a', Entity.MANIFESTATION),
        Subfield('b', Entity.MANIFESTATION),
        Subfield('c', Entity.MANIFESTATION),
        Subfield('d', Entity.MANIFESTATION),
        Subfield('e', Entity.MANIFESTATION),
        Subfield('f', Entity.MANIFESTATION),
        Subfield('g', Entity.MANIFESTATION),
        Subfield('h', Entity.MANIFESTATION),
        Subfield('j', Entity.MANIFESTATION),
        Subfield('k', Entity.MANIFESTATION),
        Subfield('l', Entity.MANIFESTATION),
        Subfield('m', Entity.MANIFESTATION),
        Subfield('n', Entity.MANIFESTATION),
        Subfield('p', Entity.MANIFESTATION),
        Subfield('q', Entity.MANIFESTATION),
        Subfield('r', Entity.MANIFESTATION),
        Subfield('z', Entity.MANIFESTATION),
    ])


class RelevantFields(Enum):
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
