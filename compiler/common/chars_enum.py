from enum import Enum


class Char(Enum):
    WHITESPACE = ' '
    NUMBER = '\d'
    LETTERS = '\w'
    PARENT = '[(]|[)]'
    STRING = '"'
    OPENING_BRACKET = '('
    CLOSING_BRACKET = ')'
    COMMA = ','