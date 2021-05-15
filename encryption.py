import hashlib
import ctypes
import numpy as np

class Encryption:

    BLOCK_SIZE = 16
    PADDING_BYTE = b'\xff'

    def __init__(self, password):

        lib = ctypes.cdll.LoadLibrary('./aes.dll')

        aes_init  = lib.aes_init
        aes_init.restype = ctypes.POINTER(ctypes.c_uint8)

        self._aes_encrypt = lib.aes_encrypt
        self._aes_encrypt.restype = None

        self._aes_decrypt = lib.aes_decrypt
        self._aes_decrypt.restype = None

        if len(password) != 0:
            try:
                hashed_key = hashlib.md5(password).digest()
            except TypeError:
                raise TypeError("a bytes-like object is required, not 'str'") from None
                
            key = np.frombuffer(hashed_key, dtype=np.uint8)

            self._key = aes_init(ctypes.c_void_p(key.ctypes.data))

        else:
            self._key = ''

    
    # def dlen_16(func):
    #     def check(self, data):
            
    #         if len(data) != 16:
    #             raise IndexError(f"Block length should be 16 bytes. Received {len(data)}.")

    #         return func(self, data)

    #     return check

    # @dlen_16
    def __enc_block(self, data_16):
        np_data = np.frombuffer(data_16, dtype=np.uint8)
        self._aes_encrypt(ctypes.c_void_p(np_data.ctypes.data), self._key)

        return np_data.tobytes()

    # @dlen_16
    def __dec_block(self, cipher_16):
        np_cipher = np.frombuffer(cipher_16, dtype=np.uint8)
        self._aes_decrypt(ctypes.c_void_p(np_cipher.ctypes.data), self._key)

        return np_cipher.tobytes()

    def encrypt(self, data: bytes):
        if self._key == '':
            return data

        cipher = b''

        while len(data) > self.BLOCK_SIZE:
            cipher += self.__enc_block(data[0:self.BLOCK_SIZE])
            data = data[self.BLOCK_SIZE:]

        data += self.PADDING_BYTE*(self.BLOCK_SIZE-len(data))
        cipher += self.__enc_block(data)
        
        return cipher
        

    def decrypt(self, cipher: bytes):
        if self._key == '':
            return cipher
        
        plain = b''

        for i in range(0, len(cipher), self.BLOCK_SIZE):
            plain += self.__dec_block(cipher[i:i+self.BLOCK_SIZE])

        return plain.replace(self.PADDING_BYTE, b'')
