class Program(object):

    context_ = []

    def __init__(self, body=None):
        self.body = body


class CallExpression(object):

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

    class Identifier(object):

        def __init__(self, name):
            self.name = name

    def enter(self, node, parent):
        expression = CallExpression(callee=self.Identifier(name=node.name))

        node.context_ = expression.arguments

        if not isinstance(parent, CallExpression):
            expression = ExpressionStatement(expression=expression)

        parent.context_.append(expression)


class NumberLiteral(object):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent.context_.append(NumberLiteral(value=node.value))


class StringLiteral(object):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent.context_.append(NumberLiteral(value=node.value))


class ExpressionStatement(object):

    def __init__(self, expression=None):
        self.expression = expression
