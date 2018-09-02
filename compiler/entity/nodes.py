class Program(object):

    def __init__(self, body=None, new_body=None):
        self.body = body
        self.new_body = new_body

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_new_body(self, new_body):
        self.new_body = new_body

    def get_new_body(self):
        return self.new_body


class CallExpression(object):

    def __init__(self, name=None, params=None):
        if params is None:
            params = []
        self.name = name
        self.params = params

    def add_param(self, param):
        self.params.append(param)


class NumberLiteral(object):

    def __init__(self, value=None):
        self.value = value

    def enter(self, node, parent):
        parent


class StringLiteral(object):

    def __init__(self, value=None):
        self.value = value


class ExpressionStatement(object):

    def __init__(self, expression=None):
        self.expression = expression
