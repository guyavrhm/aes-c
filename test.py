import ctypes
import numpy as np

key = np.array(
	[
		0x0f, 0x15, 0x71, 0xc9,
		0x47, 0xd9, 0xe8, 0x59,
		0x0c, 0xb7, 0xad, 0xd6,
		0xaf, 0x7f, 0x67, 0x98
	], 
	dtype=np.uint8
)

lib = ctypes.cdll.LoadLibrary('./aes.dll')

aes_init  = lib.aes_init
aes_init.restype = ctypes.POINTER(ctypes.c_uint8)

aes_encrypt = lib.aes_encrypt
aes_encrypt.restype = None

k = aes_init(ctypes.c_void_p(key.ctypes.data))

def enc(data):
	aes_encrypt(ctypes.c_void_p(data.ctypes.data), k)
	return data

import timeit

data = np.array(
	[
		0x01, 0x23, 0x45, 0x67,
		0x89, 0xab, 0xcd, 0xef,
		0xfe, 0xdc, 0xba, 0x98,
		0x76, 0x54, 0x32, 0x10
	], 
	dtype=np.uint8
)

start = timeit.default_timer()
for i in range(100000):
    c = enc(data)
stop = timeit.default_timer()
time = stop - start

print(time)


