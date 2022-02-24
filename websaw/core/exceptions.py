
class WebsawException(Exception):
    pass


class FixtureProcessError(WebsawException):
    pass


class HTTP(WebsawException):

    def __init__(self, status, body=None):
        self.status = status
        self.body = body
