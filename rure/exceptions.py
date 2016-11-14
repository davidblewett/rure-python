from __future__ import unicode_literals


class RegexError(Exception):
    def __init__(self, message, *args):
        super(RegexError, self).__init__(message, *args)
        self.message = str(message)


class RegexSyntaxError(RegexError):
    pass


class CompiledTooBigError(RegexError):
    pass
