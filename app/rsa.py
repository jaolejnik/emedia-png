from idat import IDAT
from rsa_support_methods import *

class RSA():
    '''
    Represents rsa algorithm
    '''

    def __init__(self, private_key):
        self.public_key = []
        self.private_key = private_key


    def encryption(self, idat_chunk):
        '''
        method to encrypt data without
        header from png file
        '''
        pass

    def decryption(self, idat_chunk):
        '''
        method to decrypt encypted
        png file
        '''
        pass

    def keys_generator(self):
        '''
        method to generate
        public and private keys
        for rsa algorithm
        '''

        p, q = generate_pq()
        n = p * q
        self.public_key.append(n)
        phi = (p - 1) * (q - 1)
        for e in range(2, phi):
            if greatest_common_divisor(e, phi) == 1:
                break
        self.public_key.append(e)
        d =  mod_inverse(e, phi)
        self.private_key = d
