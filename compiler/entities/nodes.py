from compiler.entities.nodes_interface import INodeInterface


class Program(object):

    def __init__(self, body=None):
        if body is None:
            self.body = []
        else:
            self.body = body


class CallExpression(INodeInterface):

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


class NumberLiteral(INodeInterface):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent._context.append(NumberLiteral(value=node.value))

    def exit(self, node, parent):
        pass


class StringLiteral(INodeInterface):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent._context.append(NumberLiteral(value=node.value))

    def exit(self, node, parent):
        pass


class ExpressionStatement(object):

    def __init__(self, expression=None):
        self.expression = expression


class Identifier(object):

    def __init__(self, name):
        self.name = name
