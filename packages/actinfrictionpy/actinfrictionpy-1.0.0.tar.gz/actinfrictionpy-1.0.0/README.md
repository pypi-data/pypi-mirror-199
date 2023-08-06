# Supporting python modules for dynamics analysis in "Constriction of actin rings by passive crosslinkers"

Python package for the dynamics analysis of [Ref. 1](#references).

This package is primarily for creating plots for the solutions of differential equations that are solved with another package, ([ActinFriction.jl](https://github.com/cumberworth/ActinFriction.jl)).

## Installation

This package was developed and used on Linux.
[It is available on the PyPI respository](https://pypi.org/project/actinfrictionpy/).
It can be installed by running
```
pip install actinfrictionpy
```
If you are not using a virtual environment, the `--user` flag may be used instead to install it locally to the user.
To install directly from this repository, run
```
python -m build
pip install dist/actinfrictionpy-[current version]-py3-none-any.whl
```
To run the above, it may be necessary to update a few packages:
```
python3 -m pip install --upgrade pip setuptools wheel
```

For more information on building and installing python packages, see the documentation from the [Python Packaging Authority](https://packaging.python.org/en/latest/).

## References

[1] A. Cumberworth and P. R. ten Wolde, Constriction of actin rings by passive crosslinkers, [arXiv:2203.04260 [physics.bio-ph]](https://doi.org/10.48550/arXiv.2203.04260).

## Links

[Python Packaging Authority](https://packaging.python.org/en/latest/)

[ActinFriction.jl](https://github.com/cumberworth/ActinFriction.jl)

[Replication package Ref. 1](https://doi.org/10.5281/zenodo.6327217)
