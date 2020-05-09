from contextlib import contextmanager


@contextmanager
def not_raises(exception_type):
    try:
        yield
    except exception_type as err:
        raise AssertionError(
            "Did raise exception {0} when it should not!".format(
                repr(exception_type)
            )
        )
    except Exception as err:
        raise AssertionError(
            "An unexpected exception {0} raised.".format(repr(err))
        )