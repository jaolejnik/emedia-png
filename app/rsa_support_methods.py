from math import pow
import random

def greatest_common_divisor(a, b):
    '''
    method to get gcd of
    two integers by using
    Euclidean algorithm
    '''

    if b == 0:
        return a
    else:
        return greatest_common_divisor(b, a % b)

def mod_inverse(a, m):
    '''
    method to get a modular
    multiplicative inverse of
    integer a respect to the
    modules of m
    '''

    a = a % m;
    for x in range(1, m) :
        if ((a * x) % m == 1) :
            return x
    return 1

def check_prime_number(number):
    '''
    method to check
    if number is primed
    '''

    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                return False;
        return True
    else:
        return False

def generate_prime_number():
    '''
    method to generate
    prime number
    '''

    while True:
        tmp = random.randrange(101, 201, 2)
        if check_prime_number(tmp) == True:
            prime_number = tmp
            break
    return prime_number

def generate_pq():
    '''
    method to generate different
    values of p and q
    '''

    p = generate_prime_number()
    q = generate_prime_number()
    while p == q:
        q = generate_prime_number()
    return p, q
