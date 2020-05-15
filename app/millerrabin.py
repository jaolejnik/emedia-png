import random

def miller_rabin_test(p, n):
    '''
    p - number passed for testing
    n - amount of iterations
    '''
    assert type(p) == int, "P should be int."
    assert p > 2, "P should be grater than 2"

    d = p - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(n):
        a = random.randint(2, p-2)
        x = a**d % p
        if x == 1 or x == p-1: continue
        j = 1
        while j < s and x != p-1:
            x = x**2 % p
            if x == 1: return False
            j += 1
        if x != p-1: return False

    return True

def is_prime(p, n):
    '''
    Millen-Rabin primality test
    p - number passed for testing
    n - amount of iterations
    '''
    assert type(p) == int, "P should be int."
    assert p > 2, "P should be grater than 2"

    d = p - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(n):
        a = random.randint(2, p-2)
        x = pow(a, d, p)
        if x == 1 or x == p-1: continue
        j = 1
        while j < s and x != p-1:
            x = pow(x,2 ,p)
            if x == 1: return False
            j += 1
        if x != p-1: return False

    return True

# print(miller_rabin_test(11111561, 100))
print(is_prime(11111561, 100))
