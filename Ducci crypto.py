import math
import time
import random
import myfunctions

start = time.time()

"""Key generation"""

base = [int(x) for x in input("Input starting n-tuple of odd length: ").split()]

# a = random.randint(1, myfunctions.calc_pn(base) - 1)  # quicker to use upper bound of P(n)? This would allow us to use even lengths
a = 2

D_a = list(base)  # copy of base to have `a' ducci operations

print("Private key: " + str(a))

myfunctions.repducci(a, D_a)

pub_key = [len(base), base, D_a]
print("Public key: " + str(pub_key))

"""Encryption"""

# b = random.randint(1, myfunctions.calc_pn(base) - 1)
b = 3

print("Shared secret b: " + str(b))

D_b = list(base)
D_ab = list(base)

myfunctions.repducci(b, D_b)
myfunctions.repducci(a * b, D_ab)

print("D^b: " + str(D_b))
# print("D^{ab}(u): " + str(D_ab))

D_ab_ub = myfunctions.poly_power(b, D_a)  # (1+x)^{ab} u^b
# print("(D^a(u))^b: " + str(D_ab_ub))

correction_b = list(base)  # set up original polynomial^(b-1) to be inverted
# print("Base: " + str(correction_b))

correction_b = myfunctions.poly_power(b - 1, correction_b)  # u^{b-1}
print("After power b-1: " + str(correction_b))

correction_b = myfunctions.invert_poly(correction_b)
# print("Inverted: " + str(correction_b))

D_abhope = myfunctions.poly_mult(D_ab_ub, correction_b)
print("D_ab: " + str(D_abhope))

message = [int(x) for x in input("Input message: n-tuple: ").split()]
if len(message) != len(base):
    message = [int(x) for x in input("Incorrect input length, message: ").split()]

c1 = list(D_b)
c2 = myfunctions.poly_add(message, D_ab)    # Note c2 = D^ab(u) + message

print("Cipher: c1 = " + str(D_b) + ", c2 = " + str(c2))

"""Decryption"""

c1_a_ub = myfunctions.poly_power(a, c1)
print(c1_a_ub)

correction_a = list(base)  # set up original polynomial^(a-1) to be inverted
# print("Base: " + str(correction_a))

correction_a = myfunctions.poly_power(a - 1, correction_a)  # u^{a-1}
print("After power a-1: " + str(correction_a))

correction_a = myfunctions.invert_poly(correction_a)
# print("Inverted: " + str(correction_a))

D_abhope = myfunctions.poly_mult(c1_a_ub, correction_a)
print("D_ab: " + str(D_abhope))
