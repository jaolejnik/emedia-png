from idat import IDAT
from numpy import double
from support_methods import *
from decimal import Decimal
import rsa

class RSA():
    '''
    Represents rsa algorithm
    '''

    def __init__(self, m, key_size=1024):
        self.key_size = key_size
        self.keys_generator(m)
        (self.pubkey, self.privkey) = rsa.newkeys(128)

    def keys_generator(self, m):
        '''
        method to generate
        public and private keys
        for rsa algorithm
        '''
        print("Generating keys...")
        self.public_key = []
        n = 0
        while m > n:
            p, q = generate_pq(self.key_size)
            n = p * q
        self.public_key.append(n)
        phi = (p - 1) * (q - 1)
        for e in range(2, phi):
            if greatest_common_divisor(e, phi) == 1:
                break
        self.public_key.append(e)
        print("Successfully generated public key")
        d =  mod_inverse(e, phi)
        self.private_key = int(d)
        print("Successfully generated private key")

    def encryption(self, data_to_encrypt):
        '''
        method to encrypt data without
        header from png file
        '''
        print("Encrypting...")
        encrypted_data = []
        step = self.key_size // 8 - 1 # convert to bytes
        for i in range(0, len(data_to_encrypt), step):
            raw_bytes = bytearray(data_to_encrypt[i:i+step])
            input_length = len(raw_bytes)
            int_from_bytes = int.from_bytes(raw_bytes, 'big')
            assert int_from_bytes < self.public_key[0], "M bigger that n"
            encrypted_int = pow(int_from_bytes, self.public_key[1], self.public_key[0])
            encrypted_bytes = encrypted_int.to_bytes(step+1, 'big')
            encrypted_length = len(encrypted_bytes)
            for j in range(0, input_length):
                if j < input_length-1:
                    encrypted_data.append(encrypted_bytes[j])
                else:
                    encrypted_data.append(int.from_bytes(encrypted_bytes[j:], 'big'))
        return encrypted_data

    def decryption(self, encrypted_data):
        '''
        method to decrypt encypted
        png file
        '''
        print("Decrypting...")
        decrypted_data = []
        step = self.key_size // 8 - 1 # convert to bytes
        for i in range(0, len(encrypted_data), step):
            slice = encrypted_data[i:i+step]
            encrypted_bytes = b''
            for j in range(0, len(slice)):
                if j < len(slice)-1:
                    encrypted_bytes += slice[j].to_bytes(1, 'big')
                else:
                    encrypted_bytes += slice[j].to_bytes(step-len(slice)+2, 'big')
            int_from_bytes = int.from_bytes(encrypted_bytes, 'big')
            decrypted_int = pow(int_from_bytes, self.private_key, self.public_key[0])
            decrypted_bytes = decrypted_int.to_bytes(len(slice), 'big')
            for byte in decrypted_bytes:
                decrypted_data.append(byte)
        return decrypted_data

<<<<<<< HEAD:app/own_rsa.py
    def encryption_with_ready_solution(self, data_to_encrypt):
        '''
        Method to enrypt data with
        ready python library
        '''
        print("Encrypting...")
        encrypted_data = []
        self.encrypted_rsa_bytes = []
        for data in data_to_encrypt:
            self.encrypted_rsa_bytes.append(rsa.encrypt(data.to_bytes(2, 'big'), self.pubkey))
            encrypted_data.append((float)(int.from_bytes(rsa.encrypt(data.to_bytes(2, 'big'), self.pubkey), 'big')))
        return encrypted_data

    def decryption_with_ready_solution(self, encrypted_data):
        '''
        Method to decrypt data
        with ready python library
        '''
        print("Decrypting...")
        decrypted_data = []
        for data in self.encrypted_rsa_bytes:
            decrypted_data.append(int.from_bytes(rsa.decrypt(data, self.privkey), 'big'))
        return decrypted_data

    def check_if_encryption_correct(self, data):
        '''
        Method to check
        if encrypting with
        ready solution is correct
        '''
        print("checking...")
        encrypted_data = self.encryption_with_ready_solution(data)
        decrypted_data = self.decryption_with_ready_solution(encrypted_data)
        for i in range(0, len(decrypted_data)):
            if data[i] != decrypted_data[i]:
                return False
        return True
=======

    def encryption_cbc(self, data_to_encrypt):
        '''
        method to encrypt data without
        header from png file
        '''
        print("Encrypting...")
        encrypted_data = []
        step = self.key_size // 8 - 1 # convert to bytes
        self.cbc_vector = random.getrandbits(self.key_size)
        prev_xor = self.cbc_vector
        for i in range(0, len(data_to_encrypt), step):
            raw_bytes = bytearray(data_to_encrypt[i:i+step])
            input_length = len(raw_bytes)
            int_from_bytes = int.from_bytes(raw_bytes, 'big')
            assert int_from_bytes < self.public_key[0], "M bigger that n"
            prev_xor = prev_xor.to_bytes(step+1, 'big')
            prev_xor = int.from_bytes(prev_xor[:input_length], 'big')
            xored_int = int_from_bytes ^ prev_xor
            encrypted_int = pow(xored_int, self.public_key[1], self.public_key[0])
            prev_xor = encrypted_int
            encrypted_bytes = encrypted_int.to_bytes(step+1, 'big')
            encrypted_length = len(encrypted_bytes)
            for j in range(0, input_length):
                if j < input_length-1:
                    encrypted_data.append(encrypted_bytes[j])
                else:
                    encrypted_data.append(int.from_bytes(encrypted_bytes[j:], 'big'))
        return encrypted_data


    def decryption_cbc(self, encrypted_data):
        '''
        method to decrypt encypted
        png file
        '''
        print("Decrypting...")
        decrypted_data = []
        step = self.key_size // 8 - 1 # convert to bytes
        prev_xor = self.cbc_vector
        for i in range(0, len(encrypted_data), step):
            slice = encrypted_data[i:i+step]
            encrypted_bytes = b''
            for j in range(0, len(slice)):
                if j < len(slice)-1:
                    encrypted_bytes += slice[j].to_bytes(1, 'big')
                else:
                    encrypted_bytes += slice[j].to_bytes(step-len(slice)+2, 'big')
            int_from_bytes = int.from_bytes(encrypted_bytes, 'big')
            decrypted_int=pow(int_from_bytes, self.private_key, self.public_key[0])
            prev_xor = prev_xor.to_bytes(step+1, 'big')
            prev_xor = int.from_bytes(prev_xor[:len(slice)], 'big')
            xored_int = prev_xor ^ decrypted_int
            decrypted_bytes = xored_int.to_bytes(len(slice), 'big')
            prev_xor = int_from_bytes
            for byte in decrypted_bytes:
                decrypted_data.append(byte)
        return decrypted_data
>>>>>>> 28f8142754e7db26541541f2d86ec98f40651d07:app/rsa.py
