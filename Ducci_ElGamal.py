import math
import time
import random
from myfunctions import *

def key_gen(n):
    base = random_starting_tuple(n)

    p_n = calc_pn(base)
    #a = random.randint(1, p_n - 1)
    a = math.floor(p_n/2)
    quot = [1] * len(base)

    D_a = list(base)  # initialise list of a
    D_a = repducci(a, D_a)

    pub_key = [p_n, base, D_a]
    return pub_key, a


def encrypt_ver1(pub_key, message):

    p_n, base, D_a = pub_key[0], pub_key[1], pub_key[2]
    #b = random.randint(1, p_n - 1)
    b = math.floor(p_n/3)

    D_b = list(base)
    ducci_poly_n(b, D_b)

    #print("D^b: " + str(D_b))

    D_ab = ducci_power_correction(D_a, base, b)

    c1 = list(D_b)
    c2 = poly_add(message, D_ab)    # Note c2 = D^ab(u) + message
    cipher = [c1, c2]

    return cipher


def decrypt_ver1(pub_key, priv_key, cipher):
    p_n, base, D_a = pub_key[0], pub_key[1], pub_key[2]
    a = priv_key
    c1, c2 = cipher[0], cipher[1]

    D_ab_dec = ducci_power_correction(c1, base, a)

    message_received = poly_add(D_ab_dec, c2)
    return message_received


def encrypt_ver2(pub_key, message):

    p_n, base, D_a = pub_key[0], pub_key[1], pub_key[2]
    #b = random.randint(1, p_n - 1)
    b = math.floor(p_n / 3)

    D_b = list(base)
    ducci_poly_n(b, D_b)

    c1 = list(D_b)
    c2 = replace_base_power(D_a, base, b, message)
    cipher = [c1, c2]

    return cipher


def decrypt_ver2(pub_key, priv_key, cipher):
    p_n, base, D_a = pub_key[0], pub_key[1], pub_key[2]
    a = priv_key
    c1, c2 = cipher[0], cipher[1]
    quot = [1]*len(base)

    D_ab_dec = ducci_power_correction(c1, base, a)

    base_inv = inverse(base, quot)
    ab_inv = poly_mult(D_ab_dec, base_inv)  # gives (1+x)^{ab}
    ab_inv = inverse(ab_inv, quot)

    msg_rec = poly_mult(ab_inv, c2)
    return msg_rec


def EG_ver1(n, message):
    """Compare computational times

    :param n:
    :return:
    """
    start = time.time()
    pub_key, a = key_gen(n)

    "Encrpytion"
    #message = get_msg_tuple(base)
    """message = [1,1]  # code to generate same message
    for i in range(n-2):
            message.append(0)"""

    cipher = encrypt_ver1(pub_key, message)

    "Decryption"
    msg_rec = decrypt_ver1(pub_key, a, cipher)
    end = time.time()
    return msg_rec, end-start


def EG_ver2(n, message):
    """Compare computational times

    :param n:
    :return:
    """
    start = time.time()
    pub_key, a = key_gen(n)
    p_n, base, D_a = pub_key[0], pub_key[1], pub_key[2]

    "Encrpytion"
    #message = get_msg_tuple(base)
    """message = [1,1]  # code to generate same message
    for i in range(n-2):
        message.append(0)"""

    cipher = encrypt_ver2(pub_key, message)

    "Decryption"
    msg_rec = decrypt_ver2(pub_key, a, cipher)
    end = time.time()
    time_taken = end - start
    return msg_rec, time_taken

