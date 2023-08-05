"""Module with methods for the generation of random vectors with a fixed sum of one."""
import random
import math


def sample(n: int, d: int, method: str = 'normalisation', shuffle: bool = False) -> list[list[float]]:
    """
    Generate a list of n d-dimensional random vectors whose elements sum up to one.

    Args:
        n (int): desired number of vectors.
        d (int): dimension.
        method (str): desired method (see sample_* functions in this module).
        shuffle (bool): shall each vector be randomly shuffled? Default is False.
    Returns:
        List of length n of d-dimensional lists.
    """
    assert n >= 1
    assert d >= 2

    funs = {
        'normalisation': sample_normalisation,
        'exponential': sample_exponential,
        'iterative': sample_iterative,
        'trigonometric': sample_trigonometric,
        'simplex': sample_simplex
    }
    assert method in funs.keys()

    fun = funs[method]
    vecs = fun(n, d)

    if not shuffle:
        return vecs

    return list(map(lambda e: random.sample(e, k = len(e)), vecs))


def normalise(x: list[float]) -> list[float]:
    """
    Normalise a list of floating point numbers.

    I.e., the function divides each component of the list by its sum such that
    the resulting list has sum one.

    Args:
        x (list[float]): Input list.
    Returns:
        Normalised list.
    """
    return list(map(lambda e: e / sum(x), x))


def sample_normalisation(n: int, d: int) -> list[list[float]]:
    """
    Generate a list of random vectors via normalisation.

    The process works as follows: (1) each component is sampled from a U(0,1) distribution
    and subsequently (2) each component is divided by the components' sum.

    Args:
        n (int): desired number of vectors.
        d (int): dimension.
    Returns:
        List of length n of d-dimensional lists.
    """
    assert n >= 1
    assert d >= 2

    # TODO: ugly as hell and not 'Pythonesque' at all
    vecs = [None] * n
    for i in range(n):
        vec = [random.random() for _ in range(d)]
        vecs[i] = normalise(vec)

    return vecs


def sample_iterative(n: int, d: int) -> list[list[float]]:
    """
    Generate a list of random vectors via an iterative approach.

    More precisely, the i-th component of the rpv is sampled uniformly at random from [0, s] where s is
    the sum of the 0, ..., (i-1)st components. The last component is finally (1-s). This
    way it is unsured that the vectors are normalised.

    Args:
        n (int): desired number of vectors.
        d (int): dimension.
    Returns:
        List of length n of d-dimensional lists.
    """
    assert n >= 1
    assert d >= 2

    def sample_sample_iterative(d):
        s = 0.0
        vec = [None] * d
        for j in range(d - 1):
            vec[j] = random.uniform(0, 1 - s)
            s += vec[j]
        vec[d - 1] = 1 - s
        return vec

    vecs = [sample_sample_iterative(d) for _ in range(n)]
    return list(vecs)


def sample_trigonometric(n: int, d: int) -> list[list[float]]:
    """
    Generate a list of random vectors via a trigonometric method.

    Section 5 in the following paper contains the details: Maziero, J. Generating Pseudo-Random
    Discrete Probability Distributions. Brazilian Journal of Physics 45, 377–382 (2015).
    https://doi.org/10.1007/s13538-015-0337-8)

    Args:
        n (int): desired number of vectors.
        d (int): dimension.
    Returns:
        List of length n of d-dimensional lists.
    """
    assert n >= 1
    assert d >= 2

    def sample_sample_trigonometric(d):
        ts = [random.random() for _ in range(d - 1)]

        # build vector of weights
        thetas = [None] * d
        thetas[0] = 3.1415 / 2  # pi/2
        for j in range(d - 1, 0, -1):
            thetas[j] = math.acos(math.sqrt(ts[j - 1]))

        # build the pRPV
        vec = [None] * d
        for j in range(d - 1, -1, -1):
            r = math.sin(thetas[j]) * math.sin(thetas[j])
            for k in range(j + 1, d):
                r = r * math.cos(thetas[k]) * math.cos(thetas[k])
            vec[j] = r

        return vec

    return [sample_sample_trigonometric(d) for _ in range(n)]


def sample_exponential(n: int, d: int) -> list[list[float]]:
    """
    Generate a list of random vectors by means of the inverse exponential distribution function.

    More precisely, the i-th component of the rpv is sampled
    uniformly at random from [0, s] where s is the sum of the 0, ..., (i-1)st
    components. The last component is finally (1-s). This way it is unsured that
    the vectors are normalised.

    Args:
        n (int): desired number of vectors.
        d (int): dimension.
    Returns:
        List of length n of d-dimensional lists.
    """
    assert n >= 1
    assert d >= 2

    vecs = []
    for i in range(n):
        vec = [(-1) * math.log(1 - random.random()) for _ in range(d)]
        vecs.append(normalise(vec))

    return vecs


def sample_simplex(n: int, d: int) -> list[list[float]]:
    """
    Generate a list of random vectors via simplex sampling.

    See the following paper for details on this method:
    Grimme, C. Picking a Uniformly Random Point from an Arbitrary Simplex.
    Technical Report. https://doi.org/10.13140/RG.2.1.3807.6968

    Args:
        n (int): desired number of vectors.
        d (int): dimension.
    Returns:
        List of length n of d-dimensional lists.
    """
    assert n >= 1
    assert d >= 2

    def sample_vector_from_unit_simplex(d):
        unifs = [random.random() for _ in range(d - 1)]
        unifs = sorted(unifs)

        unifs2 = [0] * (d + 1)
        for i in range(d - 1):
            unifs2[i + 1] = unifs[i]
        unifs2[d] = 1

        vec = (unifs2[i] - unifs2[i - 1] for i in range(1, d + 1))
        return vec

    vecs = [list(sample_vector_from_unit_simplex(d)) for _ in range(n)]
    return vecs
