import json

from compiler.entities.nodes_interface import INodeInterface


class Program(object):

    __slots__ = ['body', '_context']

    def __init__(self, body=None):
        if body is None:
            self.body = []
        else:
            self.body = body


class CallExpression(INodeInterface):

    __slots__ = ['name', 'params', 'callee', 'arguments']

    def __init__(self, name=None, params=None, callee=None, arguments=None):
        if params is None:
            self.params = []
        else:
            self.params = params
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.name = name
        self.callee = callee

    def enter(self, node, parent):
        expression = CallExpression(callee=Identifier(name=node.name))

        node._context = expression.arguments

        if not isinstance(parent, CallExpression):
            expression = ExpressionStatement(expression=expression)

        parent._context.append(expression)

    def exit(self, node, parent):
        pass

    def to_json(self):
        data = dict()
        for var in self.__slots__:
            data[var] = getattr(self, var)
        return json.dumps(data)


class NumberLiteral(INodeInterface):

    __slots__ = ['value']

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent._context.append(NumberLiteral(value=node.value))

    def exit(self, node, parent):
        pass


class StringLiteral(INodeInterface):

    __slots__ = ['value']

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent._context.append(NumberLiteral(value=node.value))

    def exit(self, node, parent):
        pass


class ExpressionStatement(object):

    __slots__ = ['expression']

    def __init__(self, expression=None):
        self.expression = expression


class Identifier(object):

    __slots__ = ['name']

    def __init__(self, name):
        self.name = name
