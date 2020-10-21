import math
import sympy
import random


def calc_pn(n):
    n1 = len(n)
    phi_n = sympy.totient(n1)

    for i in range(1, phi_n+1):
        myk = (2**i)%n1
        if myk == 1:
            ord_2 = i

    a = ord_2/2

    myk2 = (2**a)%n1
    if myk2 == n1-1:
        pn = n1*(2**a - 1)

    else:
        pn = 2**a - 1

    return pn


def ducci(tuple=[]):
    """one iteration of ducci sequence

    :param tuple: array/vector/n-tuple
    """

    x = tuple[0]  # hold value of first position
    y = tuple[len(tuple) - 1]
    for i in range(len(tuple) - 1):
        tuple[i] = abs(tuple[i] - tuple[i + 1])
    tuple[len(tuple) - 1] = abs(x - y)
    return tuple

def repducci(n, tuple=[]):
    """n ducci iterations

    :param n: number of Ducci iterations
    """

    for i in range(n):
        tuple = ducci(tuple)
    return tuple


def ducci_poly1(tuple=[]):
    """Multiply by (1+x) in F_2
    
    """  # same as one ducci iteration:
    # (a_0, ..., a_{n-1}) -> a_{n-1} + a_{n-1}x + ... + a_0 x^{n-1}

    g = [0] * len(tuple)
    # g will be multiplying the polynomial
    # by just x ie shifting coefficients lefts
    for i in range(len(tuple) - 1):
        g[i] = tuple[i + 1]
    g[len(tuple) - 1] = tuple[0]

    for i in range(len(tuple)):
        if tuple[i] == g[i]:
            tuple[i] = 0
        else:
            tuple[i] = 1

    return tuple


def ducci_poly_n(n, tuple=[]):
    """Multiply by (1+x)^n

    :param n: power of (1+x)
    """
    for i in range(n):
        ducci_poly1(tuple)
    return tuple


def ducci_poly_n_ver2(n, tuple):
    x1 = [0](*len(tuple)-2)
    x1.append(1)
    x1.append(1)
    print(x1)
    return poly_mult(tuple, poly_power(n, x1))



def leftshift(tuple=[]):
    """Shift the elements in array 1 spot left and takes first element to last"""

    a_0 = tuple[0]
    for i in range(len(tuple) - 1):
        tuple[i] = tuple[i + 1]
    tuple[len(tuple) - 1] = a_0
    return tuple


def mysum(n=[]):  # quicker than python sum
    """Calculate sum of array"""

    a = 0
    for i in range(len(n)):
        a += n[i]
    return a


def poly_mult(f=[], g=[]):
    """Polynomial multiplication in F_2[x]

    :param f,g: arrays where f[0] is coefficient for x^{n-1}, f[n-1] coefficient for x^0
    """
    n = len(f)
    matrix = [[0 for x in range(n)] for y in range(n)]  # n is length of tuple/polynomial degree

    for i in range(n):
        for j in range(n):
            matrix[i][j] = f[j] * g[n - 1 - i]
        for k in range(i):
            leftshift(matrix[i])

    fg = [0] * n

    for i in range(n):
        if mysum([row[i] for row in matrix]) % 2 == 0:
            fg[i] = 0
        else:
            fg[i] = 1

    if mysum(fg) == len(fg) - 1 and fg[len(fg) - 1] == 0:
        fg = [0] * (len(fg) - 1)
        fg.append(1)

    return fg


def poly_power(power, f):
    """Polynomials to the power in F_2[x]

    :param power: how many times we wish to multiply f by itself
    :param f: polynomial in array form (powers go left to right)
    """

    g = list(f)
    if power == 0:
        g = [0] * len(f)
        g[len(g) - 1] = 1

    if power > 0:
        for i in range(int(power - 1)):
            g = poly_mult(f, g)
    return g


def lead_deg(f):
    for i in range(len(f)):
        if f[i] == 1:
            deg = len(f) - 1 - i
            return deg


def deg_dif(f=[], g=[]):
    """find difference in leading degree"""

    return lead_deg(f) - lead_deg(g)


def poly_add(f=[], g=[]):
    """add/subtract polynomials g from f in F_2 ie f +/- g

    Note f, g as arrays must have same length
    """

    result = [0] * len(f)

    for i in range(len(f)):
        result[i] = abs(f[i] - g[i])
    return result


def rightshift(tuple):
    """
    shifts tuple one element to the right, same thing as multiplying by x^-1
    :param tuple:
    :return:
    """
    last = tuple[len(tuple) - 1]
    for i in range(len(tuple) - 1):
        tuple[len(tuple) - 1 - i] = tuple[len(tuple) - 2 - i]
    tuple[0] = last
    return tuple


def multiple_right_shift(tuple, n):
    """does n right shifts"""
    for i in range(n):
        rightshift(tuple)
    return tuple


def multiple_left_shift(tuple, n):
    """does n left shifts"""
    for i in range(n):
        leftshift(tuple)
    return tuple


def quotient(a, b):
    """ simple quotient with result x to power difference in degree

    :param a: polynomial in array form
    :param b: polynomial of degree less than or equal to a
    :return:
    """
    quot = lead_deg(a) - lead_deg(b)

    # multiple_left_shift(b, deg_dif) # take b to qb

    return quot


def inverse(g, f):
    """ Calculates inverse of polynomial in algebraic extension
    Note all polynomials have x^{n-1} in index 0

    :param g: polynomial we want inverse of
    :param f: quotient of ring
    :return: inverse
    """
    f_zero = [0] * len(f)
    t = list(f_zero)
    new_t = [0] * (len(f) - 1)
    new_t.append(1)

    r, new_r = f, g

    while new_r != f_zero and new_r != f:
        q = quotient(r, new_r)
        r, new_r = new_r, poly_add(r, multiple_left_shift(new_r, q))
        t, new_t = new_t, poly_add(t, multiple_left_shift(new_t, q))

    return multiple_right_shift(t, lead_deg(r))

def max_power_two(n):
    """ finds the supremum for value a where 2**a < n

    :param n: number
    :return: a
    """
    i = 0
    if n == 2:
        return 1
    if n == 1:
        return 0
    while 2**i < n/2:
        i += 1
    return i


def number_to_binary(n, width):
    """ takes a integer and expresses it as binary
    in list form (highest power of 2 is on left)

    :param n: integer greater than 0
    :param width: integer that sets the size of array
    :return: array of binary expansion
    """
    binary = [0]*width
    if (2**width-1) < n:
        print("Width too small")
        return

    while n != 0:
        power = max_power_two(n)
        binary[width - power - 1] = 1
        n = n - 2**power

    return binary


def tuple_to_number(tuple):
    """Converts binary to decimal number,

    :param tuple: n-tuple
    :return: integer
    """
    binary = 0
    for i in range(len(tuple)):
        binary += tuple[i]*2**(len(tuple) - 1 - i)
    return binary


def random_starting_tuple(length):
    """ Randomly generates a tuple of given length

    :param length: integer
    :return: tuple
    """
    rand = random.randint(1, 2**length - 1)
    start = number_to_binary(rand, length)
    return start


def ducci_mult_twobases(u, v, a, b):
    """Multiplies D^a(u) and D^b(v)

    :param u: n-tuple
    :param v: n-tuple
    :param a: integer mod period
    :param b: integer mod period
    :return: Product as n-tuple
    """
    u_func, v_func = list(u), list(v)
    x, y = repducci(a, u_func), repducci(b, v_func)
    return poly_mult(x,y)


def ducci_power_correction(D_a, u, b):
    """Takes a'th (unknown a) ducci iteration of u and
    gives the ab'th ducci iteration of u

    :param D_a: n-tuple
    :param u: starting n-tuple
    :param b: power
    :return: D^ab(u) as n-tuple
    """
    quot = [1]*len(u)   # initialise quotient of group
    D_ab_ub = poly_power(b, D_a)

    u_b1 = list(u)  # set up original polynomial u^(b-1) to be inverted
    u_b1 = poly_power(b-1, u_b1)
    u_b1 = inverse(u_b1, quot)

    D_ab = poly_mult(D_ab_ub, u_b1)

    return D_ab


def replace_base_power(D_a, u, b, msg):
    """Compute D^{ab}(msg) from D^a(u) and b

    :param D_a: a iterations of u
    :param u: starting tuple
    :param b: integer
    :param msg: message as tuple
    :return: D^{ab}(msg)
    """
    D_ab_m, quot = list(D_a), [1] * len(u)
    D_ab_m = poly_power(b, D_a)
    u_b = poly_power(b, u)
    u_b = inverse(u_b, quot)
    D_ab_m = multiple_poly_mult(D_ab_m, u_b, msg)
    return D_ab_m


def multiple_poly_mult(*arg):
    """ Multiplies each argument as polynomials

    :param arg: series of tuples
    :return: product of tuples as n-tuple
    """
    prod = [0]*(len(arg[0]) - 1)    # initialise 1 as tuple
    prod.append(1)

    for i in range(len(arg)):
        prod = poly_mult(arg[i], prod)
    return prod


def get_msg_tuple(tuple):
    """Checks if message length is same as base

    :param tuple: array
    :return: message
    """
    n = len(tuple)
    message = [int(x) for x in input("Input message: n-tuple: ").split()]

    while n != len(message):
        message = [int(x) for x in input("Wrong length. "
                                         "\nInput message: n-tuple: ").split()]

    return message


def get_msg_len(n):
    """Checks if message length is same as n

    :param tuple: array
    :return: message
    """
    message = [int(x) for x in input("Input message: n-tuple: ").split()]

    while n != len(message):
        message = [int(x) for x in input("Wrong length. "
                                         "\nInput message: n-tuple: ").split()]

    return message
