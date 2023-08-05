# Generate random vectors whose components sum up to one

This Python3 module implements different approaches [1] to randomly and uniformly generate d-dimensional vectors whose components sum up to one.

[1] Maziero, J. Generating Pseudo-Random Discrete Probability Distributions. Brazilian Journal of Physics 45, 377–382 (2015). https://doi.org/10.1007/s13538-015-0337-8


## Installation

Run the following to install the module:

```bash
pip install pyrandvec
```

## Usage

```python
from pyrandvec import sample

# Generate 10 4-dimensional vectors with the simplex-method
sample(10, 4, method = 'simplex')

# Generate 10 3-dimensional vectors with the trigonometric methdod with subsequent shuffling
sample(10, 3, method = 'trigonometric', shuffle = True)
```

# Developing randvec

To install the **pyrandvec** module along with the tools you need to develop and run test, run the following command in your *virtual environment* (virtualenv):

```bash
pip install -e .[dev]
```

