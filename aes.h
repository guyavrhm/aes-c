#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


#define ROUNDS 10
#define SIDE 4
#define SIZE 16


uint8_t *aes_init(uint8_t *key);

void aes_encrypt(uint8_t *data, uint8_t *k);

void aes_decrypt(uint8_t *cipher, uint8_t *k);