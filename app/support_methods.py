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

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def check_prime_number(number):
    '''
    method to check if number is prime
    '''
    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                return False;
        return True
    else:
        return False

def is_prime(p, n):
    '''
    Millen-Rabin primality test
    p - number passed for testing
    n - amount of iterations
    '''
    assert type(p) == int, "P should be int."
    assert p > 2, "P should be greater than 2"

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

def generate_prime_number(bit_size):
    '''
    method to generate
    prime number
    '''
    print("Generating prime number...")
    while True:
        tmp = random.getrandbits(bit_size)
        if is_prime(tmp, 10):
            prime_number = tmp
            break
    return prime_number

def generate_pq(key_size):
    '''
    method to generate different
    values of p and q
    '''
    p = generate_prime_number(key_size//2)
    q = generate_prime_number(key_size//2)
    while p == q:
        q = generate_prime_number(key_size//2)
    return p, q
