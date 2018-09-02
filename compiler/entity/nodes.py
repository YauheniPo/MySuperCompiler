class Program(object):

    def __init__(self, body=None):
        self.body = body

    def set_body(self, body):
        self.body = body


class CallExpression(object):

    def __init__(self, name, params=None):
        if params is None:
            params = []
        self.name = name
        self.params = params

    def add_param(self, param):
        self.params.append(param)


class NumberLiteral(object):

    def __init__(self, value):
        self.value = value


class StringLiteral(object):

    def __init__(self, value):
        self.value = value
