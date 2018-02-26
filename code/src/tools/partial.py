def partial(func, *args, **keywords):
    """The code of this function comes from https://docs.python.org/2/library/functools.html#functools.partial """
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(fargs + args), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
