import numpy


def ToList(args, dtype: type = None):
    if dtype is not None:
        output = numpy.atleast_1d(args).astype(dtype)
    else:
        output = numpy.atleast_1d(args)

    none_idx = numpy.where(output==None)

    if len(none_idx[0]) != 0:
        output[none_idx] = numpy.nan

    return output


# -
