from enum import Enum


class Char(Enum):
    WHITESPACE = ' '
    NUMBER = '\d'
    LETTERS = '\w'
    PARENT = '[(]|[)]'

# Парсинг - берёт сырой код и создаёт его более абстрактное представление.

# 1.1. Лексический анализ - берёт "сырой" код и разбивает его на части (токены) с помощью
#      токенизера (или лексера).
#
#      Токены — это массив маленьких объектов, которые описывают изолированый кусок кода.
#      Это могут быть цифры, пунктуация, метки, операторы, всё что угодно.
from compiler.token import Token


def tokenizer(input):
    current = 0
    tokens = []

    while(current < len(input)):
        char = input[current]

        if char is '(':
            tokens.append(Token())


# 1.2. Синтаксический анализ - берёт токены и строит представление, которое описывает
#      все части синтаксиса, и их связи между собой. Это называется промежуточным
#      представлением или AST (Abstract Syntax Tree, Абстрактное Синтаксическое Дерево).
#
#      Если кратно, то Abstract Syntax Tree (AST) — это глубоко вложенные объекты,
#      представленные таким образом, чтобы с ними было легко работать, и при этом предоставляющие
#      много информации.


# Трансформация - берёт это абстрактное представление, и делает с ним всё, что
#       требует компилятор.

# Кодогенерация берёт трансформированное представление кода, и на его основе
#      генерирует новый код.



def compiler(input):
    tokens = tokenizer(input)
    pass