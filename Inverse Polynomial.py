import myfunctions
import sympy


"""Inverse polynomials in F_2[x]/<x^{n-1}+...+1> by Euclidean algorithm"""

f = [int(x) for x in input("Input coefficients of polynomial starting with x^{n-1} on leftmost: ").split()]

mod = [1] * len(f)

mat = [mod, f]  # set up remainder matrix where first two rows are f, g
mat_mult = []  # matrix to store what we multiply by

last_coeff = (mat[len(mat) - 1][len(f) - 1])
sum_coeff = myfunctions.mysum(mat[len(mat) - 1])

while not (last_coeff == 1 and sum_coeff == 1):
    f = mat[len(mat) - 1]
    g = mat[len(mat) - 2]

    last_coeff = (mat[len(mat) - 1][len(f) - 1])  # checks remainder equal to 1
    sum_coeff = myfunctions.mysum(mat[len(mat) - 1])

    if last_coeff == 1 and sum_coeff == 1:  # stops process before appending additional remainder
        # print('Remainder now 1')
        break

    h = [0] * len(f)
    h[len(h) - 1 - myfunctions.deg_dif(f, g)] = 1  # difference in degree of f,g
    # could be refined to include polynomial besides x^n such as (1+x)
    mat_mult.append(h)

    # print("f, g: " + str(g) + str(f)) #run these to get each iteration
    # print("f * h: " + str(myfunctions.poly_mult(f, h)))

    remainder = myfunctions.poly_add(g, myfunctions.poly_mult(f, h))
    # print("remainder: " + str(remainder))

    mat.append(remainder)

print(mat)
print(mat_mult)

m = [0] * len(mat)  # create symbols to express the polynomials by
n = [0] * len(mat_mult)

for i in range(len(mat)):
    m[i] = sympy.symbols('m_{0}'.format(i))

for i in range(len(mat_mult)):
    n[i] = sympy.symbols('n_{0}'.format(i))

eq = m[len(m) - 1]

for i in range(len(n)):  # recursive algorithm for 1 in terms of f, g
    eq = eq.replace(m[len(m) - 1 - i], m[len(m) - 2 - i] * n[len(n) - 1 - i] + m[len(m) - 3 - i])
    # print(eq)

expanded_expression = sympy.expand(eq)

expanded_expression = sympy.collect(expanded_expression, (m[0], m[1]), func=sympy.factor)
print(expanded_expression)

#print("fl + gh = 1, l: " + str(sympy.collect(expanded_expression, m[0], evaluate=False)[m[0]]))  # gives l

str_inverse_g = str(sympy.collect(expanded_expression, m[1], evaluate=False)[m[1]])

print("fl + gh = 1, h: " + str(str_inverse_g))  # gives h = g^-1


"""parse str_inverse_g string"""

if '+' in str_inverse_g:
    str_inverse_g = str_inverse_g.split(' + ')

x = []
for i in range(len(str_inverse_g)):  # outer array separated by addition, inner arrays separated by multiplication
    if '*' in str_inverse_g[i]:
        x.append(str_inverse_g[i].split('*'))

    else:
        temp_list = [str_inverse_g[i]]
        x.append(temp_list)
print(x)

x_int = [[0 for i in range(len(x[j]))] for j in range(len(x))]  # new array to store indices of n

print(x_int)

"""change 3 spaces to 1 if just 1 string"""

for i in range(len(x)):     # store indices in new matrix/array x_int
    for j in range(len(x[i])):
        if x[i][j] == '1':
            x_int[i][j] = -1 # indicator for value 1
            continue
        element_str_list = x[i][j].split('_')
        x_int[i][j] = int(element_str_list[1])

print("integer x: " + str(x_int))

add_mat = [0 for i in range(len(x_int))]    # set up matrix where each element is product of polynomials as separated

for i in range(len(x_int)):
    if not x_int[i][0] == -1:
        add_mat[i] = mat_mult[x_int[i][0]]
        for j in range(1, len(x_int[i])):
            add_mat[i] = myfunctions.poly_mult(add_mat[i], mat_mult[x_int[i][j]])

    else:   # turn -1 into 1 as polynomial
        add_mat[i] = [0 for s in range(len(f) - 1)]
        add_mat[i].append(1)

print(add_mat)

inverse_g = [0 for s in range(len(f))]

for i in range(len(add_mat)):   # add each element to get inverse of given function
    inverse_g = myfunctions.poly_add(inverse_g, add_mat[i])

print(inverse_g)
