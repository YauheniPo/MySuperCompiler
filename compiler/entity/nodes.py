class Program(object):

    def __init__(self, body=None):
        self.body = body

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body


class CallExpression(object):

    def __init__(self, name=None, params=None):
        if params is None:
            params = []
        self.name = name
        self.params = params

    def add_param(self, param):
        self.params.append(param)

    def get_params(self):
        return self.params

    def enter(self, node, parent):
        parent


class NumberLiteral(object):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent


class StringLiteral(object):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent


class ExpressionStatement(object):

    def __init__(self, expression=None):
        self.expression = expression

    def set_expression(self, expression):
        self.expression = expression
