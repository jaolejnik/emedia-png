from idat import IDAT
from rsa_support_methods import *
from decimal import Decimal

class RSA():
    '''
    Represents rsa algorithm
    '''

    def __init__(self):
        self.keys_generator()

    def keys_generator(self):
        '''
        method to generate
        public and private keys
        for rsa algorithm
        '''

        self.public_key = []
        p, q = generate_pq()
        n = p * q
        self.public_key.append(n)
        phi = (p - 1) * (q - 1)
        for e in range(2, phi):
            if greatest_common_divisor(e, phi) == 1:
                break
        self.public_key.append(e)
        d =  mod_inverse(e, phi)
        self.private_key = int(d)

    def encryption(self, idat_chunk):
        '''
        method to encrypt data without
        header from png file
        '''

        encypted_data = []
        for data in idat_chunk.reconstructed_data:
            encypted_data.append((data ** self.public_key[1]) % self.public_key[0])
        return encypted_data


    def decryption(self, encrypted_data):
        '''
        method to decrypt encypted
        png file
        '''

        decrypted_data = []
        for data in encrypted_data:
            decrypted_data.append((data ** self.private_key) % self.public_key[0])
        return decrypted_data
