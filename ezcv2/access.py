def tir(*args):
    """
    The items of `*args` are rounded, converted to `int` and combined into a
    tuple.

    The primary use-case of this function is to pass point coordinates to
    certain OpenCV functions.

    >>> tir(1.24, -1.87)
    (1, -2)
    """

    return tuple(int(round(arg)) for arg in args)
