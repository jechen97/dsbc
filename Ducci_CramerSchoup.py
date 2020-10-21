from myfunctions import *
from OnewayHash import *
import random
import time
import math

def key_gen(n):
    """Generates public and private keys

    :param n: length of desired tuples
    :return: public key, private key
    """
    u = random_starting_tuple(n)
    v = random_starting_tuple(n)
    p_n = calc_pn(u)

    """a1, a2, b1, b2, c = random.randint(1, p_n - 1), \
                        random.randint(1, p_n - 1), \
                        random.randint(1, p_n - 1), \
                        random.randint(1, p_n - 1), \
                        random.randint(1, p_n - 1)"""

    a1, a2, b1, b2, c = math.floor(p_n/6), math.floor(2*p_n/6), \
                        math.floor(3*p_n/6), math.floor(4*p_n/6), math.floor(5*p_n/6)

    d, e, f = list(u), list(u), list(u)

    d = ducci_mult_twobases(u, v, a1, a2)
    e = ducci_mult_twobases(u, v, b1, b2)
    f = list(u)
    f = repducci(c, f)

    pub_key = (u, v, d, e, f)
    priv_key = (a1, a2, b1, b2, c)

    return pub_key, priv_key


def encrypt_ver1(message, pub_key):
    """Encrypts message

    :param message: n-tuple
    :param pub_key: generated public key
    :return: cipher
    """
    u, v, d, e, f = pub_key[0], pub_key[1], \
                    pub_key[2], pub_key[3], pub_key[4]
    p_n = calc_pn(u)

    g = [0]*len(u)
    while g == [0]*len(u):
        #k = random.randint(1, p_n - 1)
        k = math.floor(p_n / 3)

        D_k_u = list(u)
        D_k_u = repducci(k, D_k_u)

        D_k_v = list(v)
        D_k_v = repducci(k, D_k_v)

        D_ck_u = ducci_power_correction(f, u, k)
        g = poly_add(D_ck_u, message)

        alpha = hash_loop(D_k_u, D_k_v, g)

        uv = poly_mult(u, v)

        D_ak_uv = ducci_power_correction(d, uv, k)
        D_bk_uv = ducci_power_correction(e, uv, k)

        h = multiple_poly_mult(D_ak_uv, D_bk_uv, alpha)

    cipher = [D_k_u, D_k_v, g, h]
    return cipher


def encrypt_ver2(message, pub_key):
    """Encrypts message

    :param message: n-tuple
    :param pub_key: generated public key
    :return: cipher
    """
    u, v, d, e, f = pub_key[0], pub_key[1], \
                    pub_key[2], pub_key[3], pub_key[4]
    p_n = calc_pn(u)

    g = [0] * len(u)
    while g == [0] * len(u):
        #k = random.randint(1, p_n - 1)
        k = math.floor(p_n/3)

        D_k_u = list(u)
        D_k_u = repducci(k, D_k_u)

        D_k_v = list(v)
        D_k_v = repducci(k, D_k_v)

        g = replace_base_power(f, u, k, message)

        alpha = hash_loop(D_k_u, D_k_v, g)

        uv = poly_mult(u, v)

        D_ak_uv = ducci_power_correction(d, uv, k)
        D_bk_uv = ducci_power_correction(e, uv, k)

        h = multiple_poly_mult(D_ak_uv, D_bk_uv, alpha)

    cipher = [D_k_u, D_k_v, g, h]
    return cipher


def decrypt_ver1(pub_key, priv_key, cipher):
    u, v, d, e, f = pub_key[0], pub_key[1], \
                    pub_key[2], pub_key[3], pub_key[4]
    a1, a2, b1, b2, c = priv_key[0], priv_key[1], \
                        priv_key[2], priv_key[3], priv_key[4]
    D_k_u, D_k_v, g, h = cipher[0], cipher[1], \
                         cipher[2], cipher[3]

    alpha_dec = hash_loop(D_k_u, D_k_v, g)

    D_a1k_u = ducci_power_correction(D_k_u, u, a1)
    D_a2k_v = ducci_power_correction(D_k_v, v, a2)
    D_b1k_u = ducci_power_correction(D_k_u, u, b1)
    D_b2k_v = ducci_power_correction(D_k_v, v, b2)

    h_check = multiple_poly_mult(D_a1k_u, D_a2k_v, D_b1k_u, D_b2k_v, alpha_dec)

    if h != h_check:
        return "Failed"

    else:
        D_ck_u_dec = ducci_power_correction(D_k_u, u, c)
        message_received = poly_add(D_ck_u_dec, g)
        return message_received


def decrypt_ver2(pub_key, priv_key, cipher):
    u, v, d, e, f = pub_key[0], pub_key[1], \
                    pub_key[2], pub_key[3], pub_key[4]
    a1, a2, b1, b2, c = priv_key[0], priv_key[1], \
                        priv_key[2], priv_key[3], priv_key[4]
    D_k_u, D_k_v, g, h = cipher[0], cipher[1], \
                         cipher[2], cipher[3]
    quot = [1]*len(u)

    alpha_dec = hash_loop(D_k_u, D_k_v, g)

    D_a1k_u = ducci_power_correction(D_k_u, u, a1)
    D_a2k_v = ducci_power_correction(D_k_v, v, a2)
    D_b1k_u = ducci_power_correction(D_k_u, u, b1)
    D_b2k_v = ducci_power_correction(D_k_v, v, b2)

    h_check = multiple_poly_mult(D_a1k_u, D_a2k_v, D_b1k_u, D_b2k_v, alpha_dec)

    if h != h_check:
        return "Failed"

    else:
        D_ck_inv = ducci_power_correction(D_k_u, u, c)
        u_inv = inverse(u, quot)
        D_ck_inv = poly_mult(D_ck_inv, u_inv)
        D_ck_inv = inverse(D_ck_inv, quot)
        message_received = poly_mult(D_ck_inv, g)
        return message_received


def CrSc_ver1(n, message):
    start = time.time()
    pub_key, priv_key = key_gen(n)

    #print("Public key: " + str(pub_key))
    #print("Private key: " + str(priv_key))

    #message = get_msg_len(n)
    """message = [1,1]  # code to generate same message
    for i in range(n-2):
        message.append(0)"""

    cipher = encrypt_ver1(message, pub_key)
    #print("Cipher: " + str(cipher))

    end = time.time()
    msg_rec = decrypt_ver1(pub_key, priv_key, cipher)
    return msg_rec, end-start


def CrSc_ver2(n, message):
    start = time.time()
    pub_key, priv_key = key_gen(n)

    #print("Public key: " + str(pub_key))
    #print("Private key: " + str(priv_key))

    #message = get_msg_len(n)
    """message = [1,1]  # code to generate same message
    for i in range(n-2):
        message.append(0)"""

    cipher = encrypt_ver2(message, pub_key)
    #print("Cipher: " + str(cipher))

    end = time.time()
    msg_rec = decrypt_ver2(pub_key, priv_key, cipher)
    return msg_rec, end-start


""""Key Generation"
print("\n Key Generation")

n = int(input("Input desired length of tuples: "))

pub_key, priv_key = key_gen(n)

print("Public key: " + str(pub_key))
print("Private key: " + str(priv_key))

"Encryption"
print("\nEncryption")

message = get_msg_len(n)
p_n = calc_pn(message)

cipher = encrypt(message, pub_key)
print("Cipher: " + str(cipher))

"Decryption"
print("\nDecryption")

msg_rec = decrypt(pub_key, priv_key, cipher)
print(msg_rec)"""




