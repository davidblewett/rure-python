class RegexError(Exception):
    pass


class RegexSyntaxError(RegexError):
    pass


class CompiledTooBigError(RegexError):
    pass
