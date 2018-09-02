import re
from enum import Enum
from io import StringIO

from compiler.entity.nodes import NumberLiteral, StringLiteral, CallExpression, Program
from compiler.types import Type


class Char(Enum):
    WHITESPACE = ' '
    NUMBER = '\d'
    LETTERS = '\w'
    PARENT = '[(]|[)]'
    STRING = '"'
    OPENING_BRACKET = '('
    CLOSING_BRACKET = ')'
    COMMA = ','


# Парсинг - берёт сырой код и создаёт его более абстрактное представление.

# 1.1. Лексический анализ - берёт "сырой" код и разбивает его на части (токены) с помощью
#      токенизера (или лексера).
#
#      Токены — это массив маленьких объектов, которые описывают изолированый кусок кода.
#      Это могут быть цифры, пунктуация, метки, операторы, всё что угодно.


from compiler.token import Token


def tokenizer(input_data):
    current = 0
    tokens = []

    while current < len(input_data):
        char = input_data[current]

        if char is Char.OPENING_BRACKET.value:
            tokens.append(Token(type=Type.PAREN, value=Char.OPENING_BRACKET.value))

            current += 1

            continue

        if char is Char.CLOSING_BRACKET.value:
            tokens.append(Token(type=Type.PAREN, value=Char.CLOSING_BRACKET.value))

            current += 1

            continue

        if char in [Char.WHITESPACE.value, Char.COMMA.value]:
            current += 1
            continue

        if re.match(pattern=Char.NUMBER.value, string=char):
            value = StringIO()

            while re.match(pattern=Char.NUMBER.value, string=char):
                value.write(char)
                current += 1
                char = input_data[current]

            tokens.append(Token(type=Type.NUMBER, value=value.getvalue()))

            continue

        if char is Char.STRING:
            value = StringIO()

            while char is Char.STRING:
                value.write(char)
                current += 1
                char = input_data[current]

            current += 1
            char = input_data[current]

            tokens.append(Token(type=Type.STRING, value=value.getvalue()))

            continue

        if re.match(pattern=Char.LETTERS.value, string=char):
            value = StringIO()

            while re.match(pattern=Char.LETTERS.value, string=char):
                value.write(char)
                current += 1
                char = input_data[current]

            tokens.append(Token(type=Type.NAME, value=value.getvalue()))

            continue

        raise TypeError('I dont know what this character is: {char}'.format(char=char))

    return tokens

# 1.2. Синтаксический анализ - берёт токены и строит представление, которое описывает
#      все части синтаксиса, и их связи между собой. Это называется промежуточным
#      представлением или AST (Abstract Syntax Tree, Абстрактное Синтаксическое Дерево).
#
#      Если кратно, то Abstract Syntax Tree (AST) — это глубоко вложенные объекты,
#      представленные таким образом, чтобы с ними было легко работать, и при этом предоставляющие
#      много информации.


def parser(tokens):
    global current_parser
    current_parser = 0

    def walk():
        global current_parser
        token = tokens[current_parser]

        if token.type is Type.NUMBER:
            current_parser += 1

            return NumberLiteral(value=token.value)

        if token.type is Type.STRING:
            current_parser += 1

            return StringLiteral(value=token.value)

        if token.type is Type.PAREN and token.value is Char.OPENING_BRACKET.value:
            current_parser += 1
            token = tokens[current_parser]

            node = CallExpression(name=token.value)

            current_parser += 1
            token = tokens[current_parser]

            while token.value is not Char.CLOSING_BRACKET.value:
                node.add_param(walk())
                token = tokens[current_parser]

            current_parser += 1

            return node

        raise TypeError(token.type)

    ast = Program()

    while current_parser < len(tokens):
        ast.set_body(walk())

    return ast


def traverser(ast, visitor):
    


# Трансформация - берёт это абстрактное представление, и делает с ним всё, что
#       требует компилятор.

# Кодогенерация берёт трансформированное представление кода, и на его основе
#      генерирует новый код.


def compiler(input):
    tokens = tokenizer(input)
    ast = parser(tokens)
    pass
