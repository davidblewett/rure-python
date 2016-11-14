from functools import wraps


def accepts_bytes(f):
    """Decorator for instance methods that accept only byte strings as
    first argument.
    """
    @wraps(f)
    def wrapper(cls_instance, string, *args, **kwargs):
        caller = "'{}.{}.{}'".format(
            cls_instance.__module__,
            type(cls_instance).__name__,
            f.__name__
        )
        err_msg =  "{} requires a first argument of type 'bytes'".format(caller)
        if not isinstance(string, bytes):
            raise TypeError(err_msg)
        return f(cls_instance, string, *args, **kwargs)
    return wrapper


def accepts_string(f):
    """Decorator for instance methods that accept only unicode strings as
    first argument.
    """
    @wraps(f)
    def wrapper(cls_instance, string, *args, **kwargs):
        caller = "'{}.{}.{}'".format(
            cls_instance.__module__,
            type(cls_instance).__name__,
            f.__name__
        )
        err_msg =  "{} requires unicode string as its first argument".format(
            caller)
        if isinstance(string, bytes):
            raise TypeError(err_msg)
        return f(cls_instance, string, *args, **kwargs)
    return wrapper
