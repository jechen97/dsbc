from myfunctions import *

def seq_and(x,y):
    """Computes and logic operand for each
    corresponding element of sequence

    :param x: tuple
    :param y: tuple
    :return: tuple
    """
    n = len(x)
    res = [0]*n

    for i in range(n):
        res[i] = x[i] & y[i]
    return res


def seq_or(x, y):
    """Computes or logic operand for each
    corresponding element of sequence

    :param x: tuple
    :param y: tuple
    :return: tuple
    """
    n = len(x)
    res = [0] * n

    for i in range(n):
        res[i] = x[i] | y[i]
    return res


def seq_xor(x, y):
    """Computes xor logic operand for each
    corresponding element of sequence

    :param x: tuple
    :param y: tuple
    :return: tuple
    """
    n = len(x)
    res = [0] * n

    for i in range(n):
        res[i] = x[i] ^ y[i]
    return res


def seq_not(x):
    """Computes not logic operand for each
    corresponding element of sequence

    :param x: tuple
    :return: tuple
    """
    n = len(x)
    res = [0]*n
    for i in range(n):
        res[i] = (x[i] + 1)%2
    return x


def hash_loop(x,y,z):
    """Computes one-way hash function of tuples

    :param x: tuple
    :param y: tuple
    :param z: tuple
    :return: hash
    """

    p_n = calc_pn(x)
    n = len(x)

    if n%4 == 1:
        n1 = n-1
    if n%4 == 3:
        n1 = n-3

    z_int = (tuple_to_number(z)**2)%p_n
    h = poly_mult(x, poly_power(z_int, y))

    for i in range(1, n):
        if i <= n1/4:
            h = seq_xor(seq_or(seq_and(x,y), seq_and(seq_not(x), z)),h)

        elif i <= n1/2:
            h = seq_xor(seq_xor(seq_xor(x,y),z), h)

        elif i <= 3*n1/4:
            h = seq_xor(seq_or(seq_or(seq_and(x,y), seq_and(x,y)), seq_and(y,z)), h)

        else:
            h = seq_xor(seq_xor(seq_xor(x,y),z), h)

    return h



