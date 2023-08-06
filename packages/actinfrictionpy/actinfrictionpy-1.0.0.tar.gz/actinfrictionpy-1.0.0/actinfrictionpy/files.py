"""Classes and functions for naming calculation outputs."""

from recordclass import recordclass


def savename(prefix, params, digits=2, suffix=None, ignored_fields=[]):
    """Generate standard filename from given set of parameter key, value pairs.

    Based on the function in the Dr. Watson Julia package.
    """
    sorted_items = sorted(params._asdict().items())
    filename = [prefix]
    for key, value in sorted_items:
        if key in ignored_fields:
            pass
        elif value is None:
            pass
        elif isinstance(value, list):
            filename.append(f"{key}={value[0]}-{value[-1]}")
        elif int(value) == value:
            filename.append(f"{key}={int(value)}")
        elif isinstance(value, float):
            filename.append(f"{key}={value:.{digits}e}")
        else:
            filename.append(f"{key}={value}")

    filename = "_".join(filename)
    if suffix is not None:
        filename += f"{suffix}"

    return filename


# Record classes for model parameters
ParamsRing = recordclass(
    "ParamsRing",
    [
        "k01",
        "r01",
        "r10",
        "r12",
        "r21",
        "deltas",
        "deltad",
        "k",
        "T",
        "Nf",
        "Nsca",
        "EI",
        "Lf",
        "Df",
        "eta",
        "Ds",
        "n",
        "KsD",
        "KdD",
        "cX",
        "tend",
        "lambda0",
        "Ndtot0",
    ],
)


ParamsLinear = recordclass(
    "ParamsLinear",
    [
        "k01",
        "r01",
        "r10",
        "r12",
        "r21",
        "deltas",
        "deltad",
        "k",
        "T",
        "r0",
        "Fcond",
    ],
)


ParamsHarmonicOscillator = recordclass(
    "ParamsHarmonicOscillator",
    [
        "gamma0",
        "a",
        "k",
        "T",
    ],
)
