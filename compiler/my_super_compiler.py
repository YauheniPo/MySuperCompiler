import re
from io import StringIO

from compiler.common.chars_enum import Char
from compiler.entities.nodes import NumberLiteral, StringLiteral, CallExpression, Program
from compiler.common.types_enum import Type
from compiler.entities.token import Token


# Парсинг - берёт сырой код и создаёт его более абстрактное представление.

# 1.1. Лексический анализ - берёт "сырой" код и разбивает его на части (токены) с помощью
#      токенизера (или лексера).
#
#      Токены — это массив маленьких объектов, которые описывают изолированый кусок кода.
#      Это могут быть цифры, пунктуация, метки, операторы, всё что угодно.


def tokenizer(input_data):
    current = 0
    tokens = []

    while current < len(input_data):
        char = input_data[current]

        if char is Char.OPENING_BRACKET.value:
            tokens.append(Token(element_type=Type.PAREN, value=Char.OPENING_BRACKET.value))

            current += 1

            continue

        if char is Char.CLOSING_BRACKET.value:
            tokens.append(Token(element_type=Type.PAREN, value=Char.CLOSING_BRACKET.value))

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

            tokens.append(Token(element_type=Type.NUMBER, value=value.getvalue()))

            continue

        if char is Char.STRING:
            value = StringIO()

            while char is Char.STRING:
                value.write(char)
                current += 1
                char = input_data[current]

            current += 1
            char = input_data[current]

            tokens.append(Token(element_type=Type.STRING, value=value.getvalue()))

            continue

        if re.match(pattern=Char.LETTERS.value, string=char):
            value = StringIO()

            while re.match(pattern=Char.LETTERS.value, string=char):
                value.write(char)
                current += 1
                char = input_data[current]

            tokens.append(Token(element_type=Type.NAME, value=value.getvalue()))

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
                node.params.append(walk())
                token = tokens[current_parser]

            current_parser += 1

            return node

        raise TypeError(token.type)

    ast = Program()

    while current_parser < len(tokens):
        ast.body.append(walk())

    return ast


def traverser(ast, visitor):
    global visitor_dict
    visitor_dict = dict((type(lit).__name__, lit) for lit in visitor)

    def traverse_array(array, parent):
        if isinstance(array, list):
            [traverse_node(item, parent) for item in array]
        else:
            traverse_node(node=array, parent=parent)

    def traverse_node(node, parent):
        method = visitor_dict.get(type(node).__name__)

        if method and "enter" in dir(method):
            method.enter(node=node, parent=parent)

        def for_program():
            traverse_array(node.body, node)

        def for_call_expression():
            traverse_array(node.params, node)

        switcher = {
            "Program": for_program,
            "CallExpression": for_call_expression,
            "NumberLiteral": False,
            "StringLiteral": False
        }

        func = switcher.get(type(node).__name__)
        if func:
            func()
        elif func is False:
            pass
        else:
            raise TypeError(type(node).__name__)

        if method and "exit" in dir(method):
            method.exit(node=node, parent=parent)

    traverse_node(ast, None)


# Трансформация - берёт это абстрактное представление, и делает с ним всё, что
#       требует компилятор.


def transformer(ast):

    new_ast = Program()
    new_ast.body = ast.body

    traverser(new_ast, {NumberLiteral(), StringLiteral(), CallExpression()})

    return new_ast


# Кодогенерация берёт трансформированное представление кода, и на его основе
#      генерирует новый код.


def code_generator(node):

    def for_program():
        output = [code_generator(item) for item in node.context_]
        return '\n'.join(output)

    def for_expression_statement():
        return code_generator(node.expression) + ';'

    def for_call_expression():
        output = [code_generator(item) for item in node.arguments]
        return code_generator(node.callee) + '(' + ', '.join(output) + ')'

    def for_identifier():
        return node.name

    def for_number_literal():
        return node.value

    def for_string_literal():
        return '"' + node.value + '"'

    switcher = {
        "Program": for_program,
        "ExpressionStatement": for_expression_statement,
        "CallExpression": for_call_expression,
        "Identifier": for_identifier,
        "NumberLiteral": for_number_literal,
        "StringLiteral": for_string_literal
    }

    func = switcher.get(type(node).__name__)
    if func:
        return func()
    else:
        raise TypeError(type(node).__name__)


def compiler(input_code):

    tokens = tokenizer(input_code)
    ast = parser(tokens)
    new_ast = transformer(ast)
    output_code = code_generator(new_ast)

    return output_code
