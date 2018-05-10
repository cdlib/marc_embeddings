from enum import Enum


# See https://www.loc.gov/marc/marc-functional-analysis/original_source/appendixd.pdf
class Entity(Enum):
    WORK = 1
    EXPRESSION = 2
    MANIFESTATION = 3
    ITEM = 4
    PERSON = 5
    CORPORATE_BODY = 6
