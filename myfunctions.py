import math
import sympy

def calc_pn(n=[]):
    """ Calculate period of basic Ducci sequence

    :param n: length of tuple in Ducci sequence
    :return: return P(n)
    """
    n1 = len(n)
    prime_factors = []

    while n1 % 2 == 0:
        prime_factors.append(2)
        n1 = n1 / 2

    for i in range(3, int(math.sqrt(n1)) + 1, 2):
        while n1 % i == 0:
            prime_factors.append(i)
            n1 = int(n1 / i)

    if n1 > 2:
        prime_factors.append(n1)

    if len(n) % 2 == 1:
        """Calculate phi(n)"""
        phi_n = len(n)
        used_primes = []
        for i in range(len(prime_factors)):
            if prime_factors[i] not in used_primes:
                phi_n = phi_n * (1 - 1 / prime_factors[i])
                used_primes.append(prime_factors[i])
        phi_n = int(phi_n)

        """Find m(n) where 2**m(n) = 1 mod n"""
        for i in range(2, phi_n + 1):  # eulers totient formula
            if phi_n % i == 0 and 2 ** i % len(n) == 1:
                # print("order of 2: " + str(i))
                order_two = i

        """Calculate period of basic ducci sequence"""
        a = order_two / 2
        if 2 ** a % len(n) == len(n) - 1:
            # print("with -1")
            p_n = int(len(n) * (2 ** a - 1))

        else:
            # print("without -1")
            p_n = int(2 ** order_two - 1)

    return (p_n)


def ducci(tuple=[]):
    """one iteration of ducci sequence

    :param tuple: array/vector/n-tuple
    """

    x = tuple[0]
    y = tuple[len(tuple) - 1]
    for i in range(len(tuple) - 1):
        tuple[i] = abs(tuple[i] - tuple[i + 1])
    tuple[len(tuple) - 1] = abs(x - y)


def repducci(n, tuple=[]):
    """n ducci iterations

    :param n: number of Ducci iterations
    """

    for i in range(n):
        ducci(tuple)
    return (tuple)


def ducci_poly1(tuple=[]):
    """Multiply by (1+x)
    
    """  # same as one ducci iteration: (a_0, ..., a_{n-1}) -> a_{n-1} + a_{n-1}x + ... + a_0 x^{n-1}

    g = [0] * len(tuple)  # g will be multiplying the polynomial by just x ie shifting coefficients lefts
    for i in range(len(tuple) - 1):
        g[i] = tuple[i + 1]
    g[len(tuple) - 1] = tuple[0]

    for i in range(len(tuple)):
        if tuple[i] == g[i]:
            tuple[i] = 0
        else:
            tuple[i] = 1

    return (tuple)


def ducci_poly_n(n, tuple=[]):
    """Multiply by (1+x)^n

    :param n: power of (1+x)
    """
    for i in range(n):
        ducci_poly1(tuple)
    return (tuple)


def leftshift(tuple=[]):
    """Shift the elements in array 1 spot left and takes first element to last"""

    a_0 = tuple[0]
    for i in range(len(tuple) - 1):
        tuple[i] = tuple[i + 1]
    tuple[len(tuple) - 1] = a_0
    return (tuple)


def mysum(n=[]):  # quicker than python sum
    """Calculate sum of array"""

    a = 0
    for i in range(len(n)):
        a += n[i]
    return (a)


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

    return (fg)


def poly_power(power, f):
    """Polynomials to the power in F_2[x]

    :param power: how many times we wish to multiply f by itself
    :param f: polynomial in array form (powers go left to right)
    """

    g = list(f)
    for i in range(power-1):
        g = poly_mult(f, g)
    return (g)


def led_deg(f=[]):
    """find leading degree of polynomial f"""
    l_deg = 0
    for i in range(len(f)):
        if f[i] == 1:
            l_deg = len(f) - 1 - i
            break

    return l_deg


def deg_dif(f=[], g=[]):
    """find difference in leading degree"""

    return abs(led_deg(f) - led_deg(g))


def poly_add(f=[], g=[]):
    """add/subtract polynomials g from f in F_2 ie f +/- g

    Note f, g as arrays must have same length
    """

    result = [0] * len(f)

    for i in range(len(f)):
        result[i] = abs(f[i] - g[i])
    return result


def invert_poly(f=[]):
    """Inverse polynomials in F_2[x]/<x^{n-1}+...+1> by Euclidean algorithm"""

    mod = [1] * len(f)

    mat = [mod, f]  # set up remainder matrix where first two rows are f, g
    mat_mult = []  # matrix to store what we multiply by

    last_coeff = (mat[len(mat) - 1][len(f) - 1])
    sum_coeff = mysum(mat[len(mat) - 1])

    while not (last_coeff == 1 and sum_coeff == 1):
        f = mat[len(mat) - 1]
        g = mat[len(mat) - 2]

        last_coeff = (mat[len(mat) - 1][len(f) - 1])  # checks remainder equal to 1
        sum_coeff = mysum(mat[len(mat) - 1])

        if last_coeff == 1 and sum_coeff == 1:  # stops process before appending additional remainder
            break

        h = [0] * len(f)
        h[len(h) - 1 - deg_dif(f, g)] = 1  # difference in degree of f,g
        # could be refined to include polynomial besides x^n such as (1+x)
        mat_mult.append(h)

        remainder = poly_add(g, poly_mult(f, h))

        mat.append(remainder)

    m = [0] * len(mat)  # create symbols to express the polynomials by
    n = [0] * len(mat_mult)

    for i in range(len(mat)):
        m[i] = sympy.symbols('m_{0}'.format(i))

    for i in range(len(mat_mult)):
        n[i] = sympy.symbols('n_{0}'.format(i))

    eq = m[len(m) - 1]

    for i in range(len(n)):  # recursive algorithm for 1 in terms of f, g
        eq = eq.replace(m[len(m) - 1 - i], m[len(m) - 2 - i] * n[len(n) - 1 - i] + m[len(m) - 3 - i])

    expanded_expression = sympy.expand(eq)

    expanded_expression = sympy.collect(expanded_expression, (m[0], m[1]), func=sympy.factor)  # expanding (not sure if necessary)

    str_inverse_g = str(sympy.collect(expanded_expression, m[1], evaluate=False)[m[1]])

    """parse str_inverse_g string"""

    if '+' in str_inverse_g:
        str_inverse_g = str_inverse_g.split(' + ')

    x = []
    for i in range(len(str_inverse_g)):  # outer array separated by addition, inner arrays separated by multiplication
        if '*' in str_inverse_g[i]:
            x.append(str_inverse_g[i].split('*'))

        else:
            x.append(str_inverse_g[i])

    x_int = [[0 for i in range(len(x[j]))] for j in range(len(x))]  # new array to store indices of n

    for i in range(len(x)):  # store indices in new matrix/array x_int
        for j in range(len(x[i])):
            if not x[i][j] == '1':
                turn_to_string = str(x[i][j])
                x_int[i][j] = int(turn_to_string[2])

            else:
                x_int[i][j] = -1  # indicator for value 1

    add_mat = [0 for i in range(len(x_int))]  # set up matrix where each element is product of polynomials as separated

    for i in range(len(x_int)):
        if not x_int[i][0] == -1:
            add_mat[i] = mat_mult[x_int[i][0]]
            for j in range(1, len(x_int[i])):
                add_mat[i] = poly_mult(add_mat[i], mat_mult[x_int[i][j]])

        else:  # turn -1 into 1 as polynomial
            add_mat[i] = [0 for s in range(len(f) - 1)]
            add_mat[i].append(1)

    inverse_g = [0 for s in range(len(f))]

    for i in range(len(add_mat)):  # add each element to get inverse of given function
        inverse_g = poly_add(inverse_g, add_mat[i])

    return inverse_g
